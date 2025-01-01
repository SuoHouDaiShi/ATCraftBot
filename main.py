# import groupPoke_forTest
# 由 TWSFTS_07007 编写
# 专门用于驱动 ATCraft Sentinel Bot.请勿未经授权进行二改！
# ATCraft Network 2021-2025 ARR.
# import groupMute_forTest

import uvicorn
import autoPassRequestAndWelcomeMessage
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/")
async def root(request: Request):
    data = await request.json()  # 获取事件数据
    print(data)
    return {}

if __name__ == "__main__":
    uvicorn.run(app, port=53234)