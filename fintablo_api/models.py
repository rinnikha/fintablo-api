"""
Data models for FinTablo API entities using dataclasses.
"""

from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Union
from enum import Enum


class GroupEnum(str, Enum):
    """Enum for transaction/category groups."""

    INCOME = "income"  # Поступления
    OUTCOME = "outcome"  # Списания
    TRANSFER = "transfer"  # Переводы


def to_api_dict(obj) -> Dict[str, Any]:
    """Convert dataclass to API format dictionary."""
    result = {}
    for key, value in asdict(obj).items():
        if value is not None:
            # Handle datetime serialization - API expects dd.mm.YYYY HH:mm format
            if isinstance(value, datetime):
                value = value.strftime("%d.%m.%Y %H:%M")

            # Handle enum serialization
            if isinstance(value, Enum):
                value = value.value

            # Keys are already in camelCase, no conversion needed
            result[key] = value
    return result


@dataclass
class Category:
    """Category (Статья) model for cash flow categorization."""

    id: Optional[int] = None
    name: Optional[str] = None
    parentId: Optional[int] = None
    group: Optional[Union[GroupEnum, str]] = None  # income, outcome, transfer
    type: Optional[str] = None  # operating, financial, investment
    pnlType: Optional[str] = None
    description: Optional[str] = None
    isBuiltIn: Optional[bool] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Moneybag:
    """Moneybag (Счет) model for financial accounts."""

    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None  # nal, bank, card, electron, acquiring
    number: Optional[str] = None
    currency: Optional[str] = None
    balance: Optional[float] = None
    surplus: Optional[float] = None
    surplusTimestamp: Optional[str] = None
    groupId: Optional[int] = None
    archived: Optional[bool] = None
    hideInTotal: Optional[bool] = None
    withoutNds: Optional[bool] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Partner:
    """Partner (Контрагент) model for business partners."""

    id: Optional[int] = None
    name: Optional[str] = None
    inn: Optional[str] = None
    groupId: Optional[int] = None
    comment: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Direction:
    """Direction (Направление) model for business directions."""

    id: Optional[int] = None
    name: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Transaction:
    """Transaction (Операция ДДС) model for cash flow transactions."""

    id: Optional[int] = None
    externalId: Optional[int] = None
    value: Optional[float] = None
    moneybagId: Optional[int] = None
    group: Optional[Union[GroupEnum, str]] = None  # income, outcome, transfer
    value2: Optional[float] = None
    moneybag2Id: Optional[int] = None
    parentId: Optional[int] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    timestamp: Optional[str] = None
    isPlan: Optional[bool] = None
    categoryId: Optional[int] = None
    partnerId: Optional[int] = None
    directionId: Optional[int] = None
    dealId: Optional[int] = None
    obligationId: Optional[int] = None
    factMonth: Optional[str] = None
    spreadMonthes: Optional[List[str]] = field(default_factory=list)
    nds: Optional[float] = None
    obtainingId: Optional[int] = None
    course: Optional[int] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Deal:
    """Deal (Сделка) model for business deals."""

    id: Optional[int] = None
    name: Optional[str] = None
    jobs: List[Dict[str, Any]] = field(default_factory=list)
    goods: List[Dict[str, Any]] = field(default_factory=list)
    directionId: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    customCostPrice: Optional[float] = None
    statusId: Optional[int] = None
    partnerId: Optional[int] = None
    responsibleId: Optional[int] = None
    comment: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    actDate: Optional[str] = None
    nds: Optional[float] = None
    stages: List[Dict[str, Any]] = field(default_factory=list)

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Employee:
    """Employee (Сотрудник) model for employees."""

    id: Optional[int] = None
    name: Optional[str] = None
    date: Optional[str] = None
    positions: List[str] = field(default_factory=list)
    currency: Optional[str] = None
    regularfix: Optional[float] = None
    regularfee: Optional[float] = None
    regulartax: Optional[float] = None
    inn: Optional[str] = None
    hired: Optional[str] = None
    fired: Optional[str] = None
    comment: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Goods:
    """Goods (Товар) model for inventory items."""

    id: Optional[int] = None
    name: Optional[str] = None
    cost: Optional[float] = None
    comment: Optional[str] = None
    quantity: Optional[float] = None
    startQuantity: Optional[float] = None
    avgCost: Optional[float] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Job:
    """Job (Услуга) model for services."""

    id: Optional[int] = None
    name: Optional[str] = None
    cost: Optional[float] = None
    comment: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class Obligation:
    """Obligation (Обязательство) model for business obligations."""

    id: Optional[int] = None
    name: Optional[str] = None
    categoryId: Optional[int] = None
    directionId: Optional[int] = None
    dealId: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    statusId: Optional[int] = None
    partnerId: Optional[int] = None
    comment: Optional[str] = None
    actDate: Optional[str] = None
    nds: Optional[float] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class MoneybagGroup:
    """MoneybagGroup (Группа счетов) model."""

    id: Optional[int] = None
    name: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class PartnerGroup:
    """PartnerGroup (Группа контрагентов) model."""

    id: Optional[int] = None
    name: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class DealStatus:
    """DealStatus (Статус сделки) model."""

    id: Optional[int] = None
    name: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)


@dataclass
class ObligationStatus:
    """ObligationStatus (Статус обязательства) model."""

    id: Optional[int] = None
    name: Optional[str] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API format."""
        return to_api_dict(self)
