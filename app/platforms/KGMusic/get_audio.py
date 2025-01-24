import time

import httpx
from fastapi import HTTPException

from app.platforms.utils import cookie_to_dict


async def get_audio(self, audio_id: str):
    """
    实现获取音频功能
    :param self: 平台类
    :param audio_id: 音频链接
    :return: Bool, audio/text Bool为True时返回音频，为False时返回音频地址
    """

    base_url = 'https://wwwapi.kugou.com/play/songinfo'

    cookie = cookie_to_dict(self.headers['cookie'])

    # 构造请求参数
    params = {
        'srcappid': '2919',
        'clientver': '20000',
        'clienttime': str(round(time.time() * 1000)),
        'mid': cookie.get('kg_mid', ""),
        'uuid': cookie.get('kg_mid', ""),
        'dfid': cookie.get('kg_dfid', ""),
        'appid': '1014',
        'platid': '4',
        'encode_album_audio_id': audio_id,
        'token': '',
        'userid': '0',
    }

    # 插入签名值
    params["signature"] = self.signature(params)

    try:
        response = await self.client.get(base_url, headers=self.headers, params=params)
        response.raise_for_status()  # 检查 HTTP 状态码
        data = response.json()

        # 解析返回数据
        play_url = data.get('data', {}).get('play_url', None)
        if play_url:
            return False, play_url

    except httpx.RequestError as exc:
        # 捕获请求异常
        raise HTTPException(status_code=500, detail=f"请求失败: {str(exc)}")
    except Exception as exc:
        # 捕获其他异常
        raise HTTPException(status_code=500, detail=f"未知错误: {str(exc)}")
