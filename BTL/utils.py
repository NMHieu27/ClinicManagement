
from sqlalchemy import func
from BTL import db
from BTL.models import User, UserSex, PhieuDangKiKham, UserRole, DanhSachDangKiKham, PhieuDangKi_User, Thuoc, PhieuKhamBenh_Thuoc, PhieuKhamBenh, Rules, HoaDon
import hashlib
from sqlalchemy.sql import extract

def add_user(name, username, password, phonenumber, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                phonenumber=phonenumber,
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def get_user_by_username(username):
    user = User.query.filter(User.username.__eq__(username)).first()
    return user


def get_user_by_phone(phonenumber):
    user = User.query.filter(User.phonenumber.__eq__(phonenumber)).first()
    return user


def check_login(username, password, role=None):
    if role:
        if username and password:
            password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

            return User.query.filter(User.username.__eq__(username.strip()),
                                     User.password.__eq__(password),
                                     User.user_role.__eq__(role)).first()
    else:
        if username and password:
            password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

            return User.query.filter(User.username.__eq__(username.strip()),
                                     User.password.__eq__(password)).first()


def update_in4(id, name, sex, address, phonenumber, yearofbirth, avatar):
    user = get_user_by_id(id)
    if user:
        if name:
            user.name = name
        if sex and sex.__eq__('Nam'):
            user.sex = UserSex.MALE
        else:
            user.sex = UserSex.FEMALE
        if address:
            user.address = address
        if phonenumber:
            user.phonenumber = phonenumber
        if yearofbirth:
            user.yearofbirth = yearofbirth
        if avatar:
            user.avatar = avatar
        db.session.commit()


def load_booking_list_query():
    return PhieuDangKiKham.query.filter(PhieuDangKiKham.active.__eq__(False)).all()


def load_bill():
    return PhieuDangKiKham.query.filter(PhieuDangKiKham.active.__eq__(True),
                                        PhieuDangKiKham.tested.__eq__(True),
                                        PhieuDangKiKham.paided.__eq__(False)).all()


def get_bill_by_phieu_id(phieukham_id):
    return HoaDon.query.filter(HoaDon.phieukhambenh_id.__eq__(phieukham_id)).first()


def count_register_in_query():
    return db.session.query(PhieuDangKiKham.active, func.count(PhieuDangKiKham.id))\
            .filter(PhieuDangKiKham.active.__eq__(False)).group_by(PhieuDangKiKham.active).first()


def count_bill_in_query():
    return db.session.query(PhieuDangKiKham.active, PhieuDangKiKham.tested, PhieuDangKiKham.paided, func.count(PhieuDangKiKham.id))\
            .filter(PhieuDangKiKham.active.__eq__(True), PhieuDangKiKham.tested.__eq__(True), PhieuDangKiKham.paided.__eq__(False)).group_by(PhieuDangKiKham.active, PhieuDangKiKham.tested, PhieuDangKiKham.paided).first()


def load_booking_list_date(date):
    return PhieuDangKiKham.query.filter(PhieuDangKiKham.ngaykham.__eq__(date),
                                        PhieuDangKiKham.active.__eq__(True),
                                        PhieuDangKiKham.tested.__eq__(False)).all()


def delete_booking(booking_id):
    linked = PhieuDangKi_User.query.filter(PhieuDangKi_User.phieudangki_id.__eq__(booking_id)).all()
    for link in linked:
        db.session.delete(link)
        db.session.commit()
    phieu = PhieuDangKiKham.query.filter(PhieuDangKiKham.id.__eq__(booking_id)).first()
    db.session.delete(phieu)
    db.session.commit()


def get_date_by_booking_id(booking_id):
    phieudangkikham = PhieuDangKiKham.query.filter(PhieuDangKiKham.id.__eq__(booking_id)).first()
    return phieudangkikham.ngaykham


def count_list(date):
    danhsachdangkikham = DanhSachDangKiKham.query.filter(DanhSachDangKiKham.ngaykham.__eq__(date)).first()
    if danhsachdangkikham:
        list = db.session.query(DanhSachDangKiKham.ngaykham, func.count(PhieuDangKiKham.id))\
                            .filter(PhieuDangKiKham.ngaykham.__eq__(date),
                                    PhieuDangKiKham.active.__eq__(True))\
                            .group_by(DanhSachDangKiKham.ngaykham).first()
        if list:
            return list[1]
        else:
            return 0
    else:
        return 0


def max_patient(date):
    danhsachdangki = load_list_by_date(date)
    return danhsachdangki.max_benhnhan


def comfirm_booking(booking_id):
    phieu = PhieuDangKiKham.query.filter(PhieuDangKiKham.id.__eq__(booking_id)).first()
    phieu.active = True
    db.session.commit()


def load_doctors():
    return User.query.filter(User.user_role.__eq__(UserRole.DOCTOR)).all()

#new
def get_max_benhnhan():
    rules = Rules.query.filter().first()
    if (rules==None):
        rules = Rules()
        db.session.add(rules)
        db.session.commit()
    return rules.defaultbenhnhan

#new
def get_tien_kham():
    rules = Rules.query.filter().first()
    if (rules==None):
        rules = Rules()
        db.session.add(rules)
        db.session.commit()
    return rules.tienkham


def get_doctor_by_name(name):
    return User.query.filter(User.user_role.__eq__(UserRole.DOCTOR),
                             User.name.__eq__(name)).first()


def booking(user_id, name, phonenumber, address, yearofbirth, sex, doctor, bookingdate):
    if (sex.__eq__('Nam')):
        sex=UserSex.MALE
    else:
        sex=UserSex.FEMALE
    phieuDangKi = PhieuDangKiKham(name=name.strip(),
                                  phonenumber=phonenumber,
                                  address=address,
                                  yearofbirth=yearofbirth,
                                  sex=sex,
                                  ngaykham=bookingdate,
                                  danhsachkhambenh_id=load_list_by_date(bookingdate).id)
    db.session.add(phieuDangKi)
    db.session.commit()
    add_user_in_register(get_doctor_by_name(doctor).id, phieuDangKi.id)
    if (user_id):
        if get_user_by_id(user_id).user_role == UserRole.NURSE:
            comfirm_booking(phieuDangKi.id)
            add_user_in_register(user_id, phieuDangKi.id)
        else:
            add_user_in_register(user_id, phieuDangKi.id)


def add_user_in_register(user_id, register_id):
    phieudangki_user = PhieuDangKi_User(user_id=user_id,
                                        phieudangki_id=register_id)
    db.session.add(phieudangki_user)
    db.session.commit()


def add_phieu_kham_benh(booking_id):
    phieuKhamBenh = PhieuKhamBenh.query.filter(PhieuKhamBenh.phieudangkikham_id.__eq__(booking_id)).first()
    if (phieuKhamBenh == None):
        phieuKhamBenh = PhieuKhamBenh(phieudangkikham_id=booking_id)
        db.session.add(phieuKhamBenh)
        db.session.commit()
    return phieuKhamBenh.id


# Cập nhật phiếu khám có triệu chứng và dự đoán bệnh
def update_phieu_kham_benh(phieukham_id, trieuchung, dudoanbenh):
    phieuKhamBenh = PhieuKhamBenh.query.filter(PhieuKhamBenh.phieudangkikham_id.__eq__(phieukham_id)).first()
    if trieuchung:
        phieuKhamBenh.trieuchung = trieuchung
    if dudoanbenh:
        phieuKhamBenh.dudoanloaibenh = dudoanbenh
    db.session.commit()


def get_phieu_benh_by_phieu_dk(phieu_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.phieudangkikham_id.__eq__(phieu_id)).first()


def load_list_by_date(bookingdate):
    danhsach = DanhSachDangKiKham.query.filter(DanhSachDangKiKham.ngaykham.__eq__(bookingdate)).first()
    if (danhsach):
        return danhsach
    danhsach = DanhSachDangKiKham(ngaykham=bookingdate,
                                  max_benhnhan=get_max_benhnhan())
    db.session.add(danhsach)
    db.session.commit()
    return danhsach


def load_drugs_in_precription(precription_id):
    drugs = db.session.query(Thuoc.id, Thuoc.name, Thuoc.donvi, PhieuKhamBenh_Thuoc.soluongthuoc, PhieuKhamBenh_Thuoc.cachdung)\
                            .join(PhieuKhamBenh_Thuoc, PhieuKhamBenh_Thuoc.thuoc_id.__eq__(Thuoc.id))\
                            .filter(PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(precription_id))
    return drugs.all()


def add_phieu_kham_benh_thuoc(thuoc_id, phieukhambenh_id, soluongthuoc, cachdung):
    phieuKhamBenh_Thuoc = PhieuKhamBenh_Thuoc.query.filter(PhieuKhamBenh_Thuoc.thuoc_id.__eq__(thuoc_id), PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(phieukhambenh_id)).first()
    if ( phieuKhamBenh_Thuoc == None):
        phieuKhamBenh_Thuoc = PhieuKhamBenh_Thuoc(cachdung=cachdung,
                                                  soluongthuoc=soluongthuoc,
                                                  thuoc_id=thuoc_id,
                                                  phieukhambenh_id=phieukhambenh_id)
        db.session.add(phieuKhamBenh_Thuoc)
    else:
        phieuKhamBenh_Thuoc.cachdung=cachdung
        phieuKhamBenh_Thuoc.soluongthuoc=soluongthuoc
    db.session.commit()


#new
def load_drugs_by_id(phieu_id):
    phieuKhamBenh = PhieuKhamBenh_Thuoc.query.filter(PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(phieu_id)).all()
    result = []
    if phieuKhamBenh:
        for a in phieuKhamBenh:
            result.append(Thuoc.query.filter(Thuoc.id.__eq__(a.thuoc_id)).all())
    return result


def get_booking_by_id(booking_id):
    return PhieuDangKiKham.query.filter(PhieuDangKiKham.id.__eq__(booking_id)).first()


def load_testing_list(doctor_id=None, date=None, name=None):
    phieudangki =db.session.query(PhieuDangKiKham.id, PhieuDangKiKham.name, PhieuDangKiKham.sex, PhieuDangKiKham.yearofbirth,
                                      PhieuDangKiKham.address, PhieuDangKiKham.phonenumber, PhieuDangKiKham.ngaykham)\
                                        .join(PhieuDangKi_User, PhieuDangKiKham.id.__eq__(PhieuDangKi_User.phieudangki_id))\
                                        .filter(PhieuDangKiKham.active.__eq__(True),
                                                PhieuDangKiKham.tested.__eq__(False),
                                                PhieuDangKi_User.user_id.__eq__(doctor_id))

    if date:
        phieudangki = db.session.query(PhieuDangKiKham.id, PhieuDangKiKham.name, PhieuDangKiKham.sex,PhieuDangKiKham.yearofbirth,
                                       PhieuDangKiKham.address, PhieuDangKiKham.phonenumber, PhieuDangKiKham.ngaykham) \
                                        .join(PhieuDangKi_User, PhieuDangKiKham.id.__eq__(PhieuDangKi_User.phieudangki_id)) \
                                        .filter(PhieuDangKiKham.active.__eq__(True),
                                                PhieuDangKiKham.tested.__eq__(False),
                                                PhieuDangKiKham.ngaykham.__eq__(date),
                                                PhieuDangKi_User.user_id.__eq__(doctor_id))

    return phieudangki.all()


#new
def drugs_total(booking_id):
    booking = PhieuKhamBenh.query.filter(PhieuKhamBenh.phieudangkikham_id.__eq__(booking_id)).first().id
    phieuKhamBenh = PhieuKhamBenh_Thuoc.query.filter(PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(booking)).all()
    tong = 0
    for phieu in phieuKhamBenh:
        tong += phieu.soluongthuoc * Thuoc.query.get(phieu.thuoc_id).gia
    return tong


def create_hoa_don(tien_kham, tong_thuoc, tong_tien, booking_id, user_id):
    phieuKham_id = PhieuKhamBenh.query.filter(PhieuKhamBenh.phieudangkikham_id.__eq__(booking_id)).first().id
    hoaDon = HoaDon(tienkham=tien_kham,
                    tienthuoc=tong_thuoc,
                    tongtien=tong_tien,
                    phieukhambenh_id=booking_id,
                    yta_id=user_id)
    db.session.add(hoaDon)
    booking = get_booking_by_id(booking_id)
    booking.paided = True
    db.session.commit()


def check_tested(booking_id):
    phieuDangKiKham = PhieuDangKiKham.query.filter(PhieuDangKiKham.id.__eq__(booking_id)).first()
    phieuDangKiKham.tested = True
    db.session.commit()


def delete_drugs_in_prescription(phieukham_id, thuoc_id):
    drug = PhieuKhamBenh_Thuoc.query.filter(PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(phieukham_id),
                                            PhieuKhamBenh_Thuoc.thuoc_id.__eq__(thuoc_id)).first()
    db.session.delete(drug)
    db.session.commit()


#new
def confirm_tested(booking_id):
    booking = get_booking_by_id(booking_id)
    booking.tested = True
    db.session.commit()


def load_history_by_userId(user_id):
    phieuDangKy = PhieuDangKi_User.query.filter(PhieuDangKi_User.user_id.__eq__(user_id)).all()
    bill = []
    for phieu in phieuDangKy:
        bill.append(PhieuDangKiKham.query.filter(PhieuDangKiKham.id.__eq__(phieu.phieudangki_id)).first())
    return bill


def load_drugs():
    return Thuoc.query.filter(Thuoc.active.__eq__(True)).all()


def get_drug(drug_name):
    return Thuoc.query.filter(Thuoc.name.__eq__(drug_name)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# Thống kê, báo cáo
def get_total_revenue_month(month):
    total = db.session.query(extract('month', HoaDon.created_date), func.sum(HoaDon.tongtien))\
                                .filter(extract('month', HoaDon.created_date).__eq__(month))\
                                .group_by(extract('month', HoaDon.created_date)).first()
    if total:
        return total[1]
    else:
        return 0


# Thống kê doanh thu theo tháng
def revenue_month_stats(month):
    tongthang = get_total_revenue_month(month=month)
    return db.session.query(extract('day', HoaDon.created_date), func.count(HoaDon.id), func.sum(HoaDon.tongtien), func.sum(HoaDon.tongtien)/tongthang)\
                        .filter(extract('month', HoaDon.created_date).__eq__(month))\
                        .group_by(extract('day', HoaDon.created_date))\
                        .order_by(extract('day', HoaDon.created_date)).all()


def drug_month_stats(month):
    return db.session.query(extract('month', HoaDon.created_date), Thuoc.name, Thuoc.donvi, func.sum(PhieuKhamBenh_Thuoc.soluongthuoc), func.count(PhieuKhamBenh_Thuoc.phieukhambenh_id))\
                            .join(PhieuKhamBenh_Thuoc, PhieuKhamBenh_Thuoc.thuoc_id.__eq__(Thuoc.id))\
                            .join(PhieuKhamBenh, PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(PhieuKhamBenh.id))\
                            .join(HoaDon, PhieuKhamBenh.id.__eq__(HoaDon.phieukhambenh_id))\
                            .filter(extract('month', HoaDon.created_date).__eq__(month))\
                            .group_by(extract('month', HoaDon.created_date), Thuoc.name, Thuoc.donvi).all()


def receipt_detail(booking_id):
    return db.session.query(Thuoc.name, Thuoc.description, Thuoc.donvi, Thuoc.gia, PhieuKhamBenh_Thuoc.soluongthuoc, PhieuKhamBenh_Thuoc.cachdung)\
                            .join(PhieuKhamBenh_Thuoc, PhieuKhamBenh_Thuoc.thuoc_id.__eq__(Thuoc.id))\
                            .join(PhieuKhamBenh, PhieuKhamBenh_Thuoc.phieukhambenh_id.__eq__(PhieuKhamBenh.id))\
                            .join(PhieuDangKiKham, PhieuKhamBenh.phieudangkikham_id.__eq__(PhieuDangKiKham.id))\
                            .filter(PhieuDangKiKham.id.__eq__(booking_id)).all()