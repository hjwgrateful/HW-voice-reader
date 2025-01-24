import requests
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
API_TOKEN = os.getenv('API_TOKEN', 'your_token_here')

class APIClient:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_user_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        从API获取用户数据
        """
        url = f"{API_BASE_URL}/users/{user_id}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"获取用户 {user_id} 数据超时")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"获取用户 {user_id} 数据失败: {str(e)}")
            return None

    def post_user_data(self, user_data: Dict[str, Any]) -> bool:
        """
        向API发送用户数据
        """
        url = f"{API_BASE_URL}/users"
        
        try:
            response = self.session.post(url, json=user_data, timeout=10)
            response.raise_for_status()
            logger.info(f"成功创建用户: {user_data.get('name')}")
            return True
            
        except requests.exceptions.Timeout:
            logger.error("创建用户超时")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"创建用户失败: {str(e)}")
            return False

def main():
    client = APIClient()
    
    # 获取用户数据示例
    user = client.get_user_data(123)
    if user:
        logger.info(f"获取到用户数据: {user}")
    
    # 创建新用户示例
    new_user = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    }
    if client.post_user_data(new_user):
        logger.info("用户创建成功")

if __name__ == "__main__":
    main()