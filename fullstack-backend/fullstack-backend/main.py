import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 定义接收的数据格式（前端传过来的JSON必须长这样）
class UserCreate(BaseModel):
    username: str
    password: str

# 2. 查询接口
@app.get("/users")
def get_users():
    conn = pymysql.connect(host=os.getenv("DB_HOST", "localhost"),   # 本地跑默认 localhost，Docker 里自动读环境变量 mysql
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "123456"),  # 👈 把"123456"换成你真实的本地密码（作为本地测试的默认值）
        database=os.getenv("DB_NAME", "my_fullstack_db")
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    conn.close()
    return {"users": result}

# 3. 新增接口（Post请求）
@app.post("/users")
def add_user(user: UserCreate):
    conn = pymysql.connect(host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "123456"),  # 👈 把"123456"换成你真实的本地密码
        database=os.getenv("DB_NAME", "my_fullstack_db"))
    cursor = conn.cursor()
    # 执行插入语句
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
    conn.commit() # 千万别忘了 commit！否则数据不会真正写入
    conn.close()
    return {"status": "success", "message": "用户添加成功"}
# 4. 删除接口（Delete请求）
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = pymysql.connect(host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "123456"),  # 👈 把"123456"换成你真实的本地密码
        database=os.getenv("DB_NAME", "my_fullstack_db"))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"用户 {user_id} 删除成功"}