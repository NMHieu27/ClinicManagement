from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Enum, ForeignKey,Date
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
from BTL import db

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 11
    NURSE = 22
    DOCTOR = 33
    USER = 44


class UserSex(UserEnum):
    MALE = 0
    FEMALE = 1


class Rules(BaseModel):
    __tablename__ = 'rules'

    defaultbenhnhan = Column(Integer, default=30)
    tienkham = Column(Float, default=100000)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    sex = Column(Enum(UserSex), default=UserSex.MALE)
    yearofbirth = Column(Date, default=datetime.now())
    address = Column(String(500), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    phonenumber = Column(String(10), nullable=False, unique=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    # 1 phiếu được 3 người tham gia đăng kí tạo nên (người dùng, y ta xac nhan, bac si (người dùng chọn bác sĩ khi đăng kí)),
    # 1 người tham đăng kí nhiều phiếu đăng kí khám --> n-n
    phieudangki_user = relationship('PhieuDangKi_User', backref='user', lazy=True)
    hoadon_yta = relationship('HoaDon', backref='user', lazy=True) # hoa don duoc y ta thanh toan

    def __str__(self):
        return self.name


class DanhSachDangKiKham(BaseModel):
    __tablename__ = 'danhsachdangkikham'

    max_benhnhan = Column(Integer, default=30 )
    ngaykham = Column(Date, default=datetime.now())
    phieudangki = relationship('PhieuDangKiKham', backref='danhsachdangkikham', lazy=True)



class PhieuDangKiKham(BaseModel):
    __tablename__ = 'phieudangkikham'

    name = Column(String(50), nullable=False)
    sex = Column(Enum(UserSex), default=UserSex.MALE)
    phonenumber = Column(String(10), nullable=False)
    yearofbirth = Column(Date, default=datetime.now())
    address = Column(String(500), nullable=False)
    ngaydat = Column(DateTime, default=datetime.now())
    ngaykham = Column(Date, default=datetime.now())
    active = Column(Boolean, default=False)
    tested = Column(Boolean, default=False)
    paided = Column(Boolean, default=False)
    danhsachkhambenh_id = Column(Integer, ForeignKey(DanhSachDangKiKham.id), nullable=False, primary_key=True)
    phieudangki_user = relationship('PhieuDangKi_User', backref='phieudangkikham', lazy=True)
    phieudangki_phieukham = relationship('PhieuKhamBenh', backref='phieudangkikham', lazy=True)


    def __str__(self):
        return self.name


class PhieuDangKi_User(db.Model):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    phieudangki_id = Column(Integer, ForeignKey(PhieuDangKiKham.id), nullable=False, primary_key=True)


class Thuoc(BaseModel):
    __tablename__ = 'thuoc'

    name = Column(String(50), nullable=False)
    description = Column(String(5000), nullable= False)
    donvi = Column(String(50), nullable=False)
    gia = Column(Float, default=0)
    active = Column(Boolean, default=True)
    phieukhambenh_thuoc = relationship('PhieuKhamBenh_Thuoc', backref='thuoc', lazy=True)

    def __str__(self):
        return self.name


class PhieuKhamBenh(BaseModel):
    __tablename__ = 'phieukhambenh'

    trieuchung = Column(String(500), nullable=True)
    dudoanloaibenh = Column(String(500), nullable=True)
    phieudangkikham_id = Column(Integer, ForeignKey(PhieuDangKiKham.id), nullable=False, primary_key=True)
    phieukham_thuoc = relationship('PhieuKhamBenh_Thuoc', backref='phieukhambenh', lazy=True)
    hoadons = relationship('HoaDon', backref='phieukhambenh', lazy=True)


class PhieuKhamBenh_Thuoc(db.Model):
    soluongthuoc = Column(Integer, default=0)
    cachdung = Column(String(500), nullable=False)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False, primary_key=True)
    phieukhambenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False, primary_key=True)


class HoaDon(BaseModel):
    __tablename__ = 'hoadon'

    tienkham = Column(Float, default= 100000 )
    tienthuoc = Column(Float, default=0)
    tongtien = Column(Float, default=0)
    created_date = Column(DateTime, default=datetime.now())
    #tham chieu den phieu kham benh de lay ten benh nhan, thuoc ke toa
    phieukhambenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False, primary_key=True)
    yta_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)


if __name__ == '__main__':
    db.create_all()
