# generated by datamodel-codegen:
#   filename:  catalog.template.schema.json
#   timestamp: 2021-03-15T04:21:58+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr


class Kind(Enum):
    Component = 'Component'
    API = 'API'
    Resource = 'Resource'


class Metadata(BaseModel):
    namespace: Optional[str] = None
    name: constr(regex=r'^[a-zA-Z0-9_-]*$')
    description: str
    labels: Optional[Dict[str, Any]] = None
    tags: Optional[List[constr(regex=r'^[a-zA-Z0-9-]*$')]] = None


class Type(Enum):
    service = 'service'
    website = 'website'
    library = 'library'


class Lifecycle(Enum):
    experimental = 'experimental'
    production = 'production'
    deprecated = 'deprecated'


class Spec(BaseModel):
    type: Type
    lifecycle: Lifecycle
    owner: List[constr(regex=r'@gmail.com.br')]


class Model(BaseModel):
    apiVersion: str
    manifestVersion: Optional[str] = None
    kind: Kind
    metadata: Metadata
    spec: Spec
