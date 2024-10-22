from typing import Optional

from pydantic import BaseModel


class PuaUserContract(BaseModel):
    Id: int
    Nombre: str
    Usuario: str
    Correo: str
    EsCliente: bool
    CodigoSap: Optional[str]
    Token: str
    Activo: bool
    TipoUsuario: Optional[str]
