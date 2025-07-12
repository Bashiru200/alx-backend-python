from importlib import import_module
from typing import List, Dict, Any, Generator

# Import the single‑row generator from the first module
stream_mod = import_module("0-stream_users")


def stream_users_in_batches(
    batch_size: int = 50,
) -> Generator[List[Dict[str, Any]], None, None]:
    """Yield *lists* of users, `batch_size` rows at a time.

    Uses exactly one loop to iterate over ``stream_users`` and accumulates rows
    into a list until the requested size is reached, then yields that list. A
    final (smaller) batch is yielded at the end.
    """

    batch: List[Dict[str, Any]] = []

    for user in stream_mod.stream_users():  # 1️⃣ first loop (over rows)
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:  # leftovers after generator exhausts
        yield batch


def batch_processing(batch_size: int = 50) -> List[Dict[str, Any]]:
    """Process each batch and return users over age 25.

    Constraints:
    * total ≤3 loops (we will use a second loop over batches and a third loop
      inside each batch).
    * reuses ``stream_users_in_batches``.
    """

    filtered: List[Dict[str, Any]] = []

    for batch in stream_users_in_batches(batch_size):  # 2️⃣ second loop (batches)
        for user in batch:                            # 3️⃣ third loop (within batch)
            if user["age"] > 25:
                filtered.append(user)

    return filtered


if __name__ == "__main__":
    # quick manual test
    users_over_25 = batch_processing(30)
    print(f"Found {len(users_over_25)} users over 25. Sample:")
    for u in users_over_25[:5]:
        print(u)
