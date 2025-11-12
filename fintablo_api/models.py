"""Data models for FinTablo API entities using dataclasses."""

from datetime import datetime
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Dict, Any, List, Optional, Union
from enum import Enum


class GroupEnum(str, Enum):
    """Enum for transaction/category groups."""

    INCOME = "income"  # Поступления
    OUTCOME = "outcome"  # Списания
    TRANSFER = "transfer"  # Переводы


def _serialize_value(value: Any) -> Any:
    """Recursively serialize values for API consumption."""
    if value is None:
        return None

    if isinstance(value, datetime):
        # API expects datetimes as dd.mm.YYYY HH:mm
        return value.strftime("%d.%m.%Y %H:%M")

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, list):
        serialized_list = []
        for item in value:
            serialized_item = _serialize_value(item)
            if serialized_item is not None:
                serialized_list.append(serialized_item)
        return serialized_list

    if isinstance(value, dict):
        serialized: Dict[str, Any] = {}
        for key, item in value.items():
            serialized_item = _serialize_value(item)
            if serialized_item is not None:
                serialized[key] = serialized_item
        return serialized

    if is_dataclass(value):
        return to_api_dict(value)

    if hasattr(value, "to_api_dict"):
        return value.to_api_dict()

    return value


def to_api_dict(obj: Any) -> Dict[str, Any]:
    """Convert dataclass instance to API-ready dictionary."""
    if not is_dataclass(obj):
        raise TypeError("to_api_dict expects a dataclass instance")

    result: Dict[str, Any] = {}
    for field_obj in fields(obj):
        value = getattr(obj, field_obj.name)
        serialized = _serialize_value(value)
        if serialized is not None:
            result[field_obj.name] = serialized
    return result


class ApiModel:
    """Mixin providing API serialization."""

    def to_api_dict(self) -> Dict[str, Any]:
        return to_api_dict(self)


@dataclass
class Category(ApiModel):
    """Category (Статья) model for cash flow categorization."""

    id: Optional[int] = None
    name: Optional[str] = None
    parentId: Optional[int] = None
    group: Optional[Union[GroupEnum, str]] = None  # income, outcome, transfer
    type: Optional[str] = None  # operating, financial, investment
    pnlType: Optional[str] = None
    description: Optional[str] = None
    isBuiltIn: Optional[bool] = None

@dataclass
class Moneybag(ApiModel):
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

@dataclass
class Partner(ApiModel):
    """Partner (Контрагент) model for business partners."""

    id: Optional[int] = None
    name: Optional[str] = None
    inn: Optional[str] = None
    groupId: Optional[int] = None
    comment: Optional[str] = None

@dataclass
class Direction(ApiModel):
    """Direction (Направление) model for business directions."""

    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class Transaction(ApiModel):
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

@dataclass
class Deal(ApiModel):
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

@dataclass
class Employee(ApiModel):
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

@dataclass
class Goods(ApiModel):
    """Goods (Товар) model for inventory items."""

    id: Optional[int] = None
    name: Optional[str] = None
    cost: Optional[float] = None
    comment: Optional[str] = None
    quantity: Optional[float] = None
    startQuantity: Optional[float] = None
    avgCost: Optional[float] = None



@dataclass
class Job(ApiModel):
    """Job (Услуга) model for services."""

    id: Optional[int] = None
    name: Optional[str] = None
    cost: Optional[float] = None
    comment: Optional[str] = None

@dataclass
class Obligation(ApiModel):
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

@dataclass
class MoneybagGroup(ApiModel):
    """MoneybagGroup (Группа счетов) model."""

    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class PartnerGroup(ApiModel):
    """PartnerGroup (Группа контрагентов) model."""

    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class DealStatus(ApiModel):
    """DealStatus (Статус сделки) model."""

    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class ObligationStatus(ApiModel):
    """ObligationStatus (Статус обязательства) model."""

    id: Optional[int] = None
    name: Optional[str] = None
