from typing import Protocol, Any, Iterable
from rag_system.backend.storage import StorageProvider

from fastapi import Depends, HTTPException, Request, status


class UserProvider(Protocol):
    async def get_verified_user(self, request: Request) -> Any: ...

    async def get_admin_user(self, request: Request) -> Any: ...


class PermissionProvider(Protocol):
    def has_access(
        self,
        user_id: str,
        access_type: str = "write",
        access_control: dict | None = None,
        user_group_ids: set[str] | None = None,
        strict: bool = True,
        db: Any | None = None,
    ) -> bool: ...

    def has_permission(
        self,
        user_id: str,
        permission_key: str,
        default_permissions: dict,
        db: Any | None = None,
    ) -> bool: ...

    def get_users_with_access(
        self,
        access_type: str = "write",
        access_control: dict | None = None,
        db: Any | None = None,
    ) -> list[Any]: ...


def _get_provider(request: Request, attr: str):
    provider = getattr(request.app.state, attr, None)
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG provider not configured: {attr}",
        )
    return provider


def get_user_provider(request: Request) -> UserProvider:
    return _get_provider(request, "rag_user_provider")


def get_permission_provider(request: Request) -> PermissionProvider:
    return _get_provider(request, "rag_permission_provider")


def get_session_provider(request: Request):
    return _get_provider(request, "rag_get_session")


def get_storage_provider(request: Request) -> StorageProvider:
    return _get_provider(request, "rag_storage_provider")


async def get_verified_user(
    request: Request, provider: UserProvider = Depends(get_user_provider)
):
    return await provider.get_verified_user(request)


async def get_admin_user(
    request: Request, provider: UserProvider = Depends(get_user_provider)
):
    return await provider.get_admin_user(request)


def get_session(request: Request, provider=Depends(get_session_provider)):
    yield from provider()
