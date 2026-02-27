import requests
from sqlalchemy import select

from app.config import CENTRAL_API_URL, CENTRAL_API_TOKEN
from app.models import StationTask
from app.database import AsyncSessionLocal
from datetime import datetime


async def sync_tasks():
    print("=== SYNC STARTED ===")

    headers = {"X-Station-Token": CENTRAL_API_TOKEN}

    try:
        response = requests.get(
            f"{CENTRAL_API_URL}/api/agg/station/tasks",
            headers=headers,
            timeout=10
        )
    except Exception as e:
        print("SYNC ERROR: request failed:", e)
        return False

    print("SYNC: status code =", response.status_code)

    if response.status_code != 200:
        print("SYNC: bad response, body:", response.text)
        return False

    data = response.json()
    print("SYNC: tasks received =", len(data))

    async with AsyncSessionLocal() as db:

        for item in data:
            print("SYNC: processing task_id =", item["task_id"])

            result = await db.execute(
                select(StationTask).where(
                    StationTask.server_task_id == item["task_id"]
                )
            )
            exists = result.scalar_one_or_none()

            if exists:
                print("SYNC: updating:", item["task_id"])
                exists.production_date = (
                    datetime.strptime(item["production_date"], "%Y-%m-%d").date()
                    if item.get("production_date")
                    else None
                )
                exists.shelf_life_days = item["product"].get("shelf_life_days")
                continue

            print("SYNC: inserting:", item["task_id"])

            task = StationTask(
                server_task_id=item["task_id"],
                product_name=item["product"]["name"],
                gtin=item["product"]["gtin"],
                quantity_in_box=item["product"]["quantity_in_box"],
                quantity_in_pallet=item["product"]["quantity_in_pallet"],
                planned_quantity=item["planned_quantity"],
                production_date=(
                    datetime.strptime(item["production_date"], "%Y-%m-%d").date()
                    if item.get("production_date")
                    else None
                ),
                shelf_life_days=item["product"].get("shelf_life_days"),
                scenario_code=item["scenario"]["code"],
                scenario_name=item["scenario"]["name"],
                status="queued"
            )
            db.add(task)

        print("SYNC: committing...")
        await db.commit()

    print("=== SYNC FINISHED ===")
    return True