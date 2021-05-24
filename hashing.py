from passlib.context import CryptContext

#Hash password ในที่นี้ใช้ md5 เป็น Hash Function
pwd_cxt = CryptContext(schemes=['md5_crypt'],deprecated = 'auto')

#สร้าง Class สำหรับทำการ Hash password โดยมี 2 Function
class Hash():

    #1.Function สำหรับการ becrypt password
    def becrypt(password : str):
        return pwd_cxt.hash(password)

    #2. Function สำหรับการ Verify password โดยเทียบ plain password กับ hash password ถ้า True คือทั้ง 2 ค่าเท่ากัน
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)