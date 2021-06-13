from typing import Any, Callable, Optional, TypeVar

from fastapi import params

R_T = TypeVar("R_T")


def Depends(
    dependency: Optional[Callable[..., R_T]] = None, *, use_cache: bool = True
) -> R_T:
    return params.Depends(dependency=dependency, use_cache=use_cache)  # type: ignore
