# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Interface for the Market data."""

import abc
import datetime
from typing import Any, List, Tuple, Callable

import tensorflow.compat.v2 as tf

from tf_quant_finance.experimental.pricing_platform.framework import curve_types

from tf_quant_finance.experimental.pricing_platform.framework import interpolation_method
from tf_quant_finance.experimental.pricing_platform.framework import types
from tf_quant_finance.experimental.pricing_platform.instrument_protos import period_pb2


class RateCurve(abc.ABC):
  """Interface for interest rate curves."""

  @abc.abstractmethod
  def discount_factor(self,
                      date: types.DateTensor,
                      **kwargs) -> tf.Tensor:
    """Returns the discount factor to a specified set of dates.

    Args:
      date: The dates at which to evaluate the discount factors.
      **kwargs: The context object, e.g., curve_type.

    Returns:
      A `Tensor` of the same shape as `dates` with the corresponding discount
      factors.
    """
    pass

  @abc.abstractmethod
  def forward_rate(self,
                   start_date: types.DateTensor,
                   end_date: types.DateTensor,
                   **kwargs) -> tf.Tensor:
    """Returns the simply accrued forward rate between dates.

    Args:
      start_date: A `DateTensor` specifying the start of the accrual period
        for the forward rate.
      end_date: A `DateTensor` specifying the end of the accrual period
        for the forward rate. The shape of `maturity_date` must be broadcastable
        with the shape of `start_date`.
      **kwargs: The context object, e.g., curve_type.

    Returns:
      A `Tensor` with the corresponding forward rates.
    """
    pass

  @abc.abstractmethod
  def discount_rate(self,
                    date: types.DateTensor,
                    context=None) -> tf.Tensor:
    """Returns the discount rates to a specified set of dates.

    Args:
      date: The dates at which to evaluate the discount rates.
      context: The context object, e.g., curve_type.

    Returns:
      A `Tensor` of the same shape as `dates` with the corresponding discount
      rates.
    """
    pass

  @property
  @abc.abstractmethod
  def curve_type(self) ->Any:  # to be specified
    """Returns type of the curve."""
    pass

  @abc.abstractmethod
  def interpolation_method(self) -> interpolation_method.InterpolationMethod:
    """Interpolation method used for this discount curve."""
    pass

  @abc.abstractmethod
  def discount_factors_and_dates(self) -> Tuple[types.FloatTensor,
                                                types.DateTensor]:
    """Returns discount factors and dates at which the discount curve is fitted.
    """
    pass

  @abc.abstractproperty
  def discount_factor_nodes(self) -> types.FloatTensor:
    """Discount factors at the interpolation nodes."""
    pass

  @abc.abstractmethod
  def set_discount_factor_nodes(self,
                                values: types.FloatTensor) -> types.FloatTensor:
    """Update discount factors at the interpolation nodes with new values."""
    pass

  @abc.abstractproperty
  def discount_rate_nodes(self) -> types.FloatTensor:
    """Discount rates at the interpolation nodes."""
    pass

  @abc.abstractproperty
  def node_dates(self) -> types.DateTensor:
    """Dates at which the discount factors and rates are specified."""
    return self._dates

  @abc.abstractproperty
  def daycount_convention(self) -> types.DayCountConventionsProtoType:
    """Daycount convention."""
    raise NotImplementedError

  @abc.abstractmethod
  def daycount_fn(self) -> Callable[..., Any]:
    """Daycount function."""
    raise NotImplementedError


class ProcessedMarketData(abc.ABC):
  """Market data snapshot used by pricing library."""

  @abc.abstractproperty
  def date(self) -> datetime.date:
    """The date of the market data."""
    pass

  @abc.abstractproperty
  def time(self) -> datetime.time:
    """The time of the snapshot."""
    pass

  @abc.abstractmethod
  def yield_curve(self, curve_type: curve_types.CurveType) -> RateCurve:
    """The yield curve object."""
    pass

  @abc.abstractmethod
  def fixings(self,
              date: types.DateTensor,
              fixing_type: str,
              tenor: period_pb2.Period) -> tf.Tensor:
    """Returns past fixings of the market rates at the specified dates."""
    pass

  @abc.abstractmethod
  def spot(self, asset: str,
           data: types.DateTensor) -> tf.Tensor:
    """The spot price of an asset."""
    pass

  @abc.abstractmethod
  def volatility_surface(self, asset: str) -> Any:  # To be specified
    """The volatility surface object for an asset."""
    pass

  @abc.abstractmethod
  def forward_curve(self, asset: str) -> RateCurve:
    """The forward curve of the asset prices object."""
    pass

  @abc.abstractproperty
  def supported_currencies(self) -> List[str]:
    """List of supported currencies."""
    pass

  @abc.abstractmethod
  def supported_assets(self) -> List[str]:
    """List of supported assets."""
    pass

  @abc.abstractproperty
  def dtype(self) -> types.Dtype:
    """Type of the float calculations."""
    pass


__all__ = ["RateCurve", "ProcessedMarketData"]

