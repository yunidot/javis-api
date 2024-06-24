from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, DateTime
from src.database import Base


class User(Base):
    __tablename__ = 'com_user'
    # 사용자 아이디
    user_id: str | Column = Column(String(50), name="user_id", nullable=False, unique=True, primary_key=True)
    # 사용자 이메일 주소 (ID)
    email_addr: str | Column = Column(String(255), name="email_addr", nullable=False)
    # 사용자 이름
    user_nm: str | Column = Column(String(100), name="user_nm", nullable=False)
    # 사용자 비밀번호
    user_pwd: str | Column = Column(String(255), name="user_pwd", nullable=True)
    # 사용 여부
    use_yn: str | Column = Column(String(1), name="use_yn", nullable=False, default="Y")
    # 생성일자
    created_at: datetime | Column = Column(DateTime(timezone=True), name="created_at", nullable=False)
    # 생성자
    created_by: str | Column = Column(String(50), name="created_by", nullable=False)
    # 최종 수정일자
    updated_at: datetime | Column = Column(DateTime(timezone=True), name="updated_at", nullable=True)
    # 최종 수정자
    updated_by: str | Column = Column(String(50), name="updated_by", nullable=True)
    # 비밀번호 등록일
    password_at: datetime | Column = Column(DateTime(timezone=True), name="password_at", nullable=True)
    # SNS 로그인 연동 (naver)
    use_naver_auth_yn: str | Column = Column(String(1), name="use_naver_auth_yn", default="N")
    # SNS 로그인 연동 여부 (Kakao)
    use_kakao_auth_yn: str | Column = Column(String(1), name="use_kakao_auth_yn", default="N")
    # SNS 로그인 연동 여부 (Google)
    use_google_auth_yn: str | Column = Column(String(1), name="use_google_auth_yn", default="N")
