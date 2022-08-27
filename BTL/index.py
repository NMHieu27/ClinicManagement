
from BTL import app, login
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user
import utils
from  datetime import datetime
import cloudinary.uploader

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        try:
            name = request.form.get('name')
            username = request.form.get('username')
            if utils.get_user_by_username(username=username):
                err_msg = 'Username đã được sử dụng!!!!'
                return render_template('register.html', err_msg=err_msg)
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            phonenumber = request.form.get('phonenumber')
            if utils.get_user_by_phone(phonenumber=phonenumber):
                err_msg= 'Số điện thoại đã được sử dụng để đăng kí!!!!'
                return render_template('register.html', err_msg=err_msg)
            avatar_path = None
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, phonenumber=phonenumber, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = 'Mật khẩu không khớp!!!!'
        except Exception as ex:
            err_msg = 'He thong co loi: ' + str(ex)
    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username, password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = 'Username hoặc password không chính xác!!!'
    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']
    user = utils.check_login(username=username,
                            password=password,
                            role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/user-update', methods=['get', 'post'])
def user_update():
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        sex = request.form.get('sex')
        address = request.form.get('address')
        phonenumber = request.form.get('phonenumber')
        if utils.get_user_by_phone(phonenumber=phonenumber):
            err_msg = 'Số điện thoại đã được sử dụng để đăng kí!!!!'
            return render_template('user/userupdate.html', err_msg=err_msg)
        yearofbirth = request.form.get('birth')
        avatar = request.files.get('avatar')
        avatar_path = None
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            avatar_path = res['secure_url']
        utils.update_in4(id=session.get('_user_id'), name=name, sex=sex, address=address, phonenumber=phonenumber, yearofbirth=yearofbirth, avatar=avatar_path)
        return redirect(url_for('user_update'))
    else:
        return render_template('user/userupdate.html')


@app.route('/user-history', methods=['get', 'post'])
def user_history():
    booking_list = utils.load_history_by_userId(user_id=session.get('_user_id'))
    return render_template('user/history.html', booking_list=booking_list)


@app.route('/user-history/bill-detail')
def bill_detail():
    phieu_id = request.args.get('booking_id')
    booking = utils.get_booking_by_id(phieu_id)
    hoadon = utils.get_bill_by_phieu_id(phieu_id)
    drugs = utils.receipt_detail(phieu_id)
    return render_template('user/billdetail.html', booking=booking, hoadon=hoadon, drugs=drugs)


@app.route('/user-booking', methods=['get', 'post'])
def user_booking():
    doctors = utils.load_doctors()
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phonenumber = request.form.get('tel')
        address = request.form.get('address')
        yearofbirth = request.form.get('birth')
        sex = request.form.get('sex')
        bookingdate = request.form.get('date')
        doctor = request.form.get('doctor')
        if ( utils.max_patient(date=bookingdate) == utils.count_list(date=bookingdate)):
            err_msg = 'Ngày chọn khám đã đầy, mời bạn chọn ngày khác!!!'
        else:
            utils.booking(user_id=session.get('_user_id'), name=name, phonenumber=phonenumber, address=address, yearofbirth=yearofbirth, sex=sex, doctor=doctor, bookingdate=bookingdate)
            return redirect(url_for('user_booking'))
    return render_template('user_booking.html', doctors=doctors, err_msg=err_msg)


@app.route('/booking-list', methods=['get', 'post'])
def booking_list():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    booking_list = utils.load_booking_list_date(date=date)
    return render_template('nurse/list.html', booking_list=booking_list, date=date)


@app.route('/delete-booking')
def delete_booking():
    date = request.args.get('date')
    booking_id=request.args.get('booking_id')
    utils.delete_booking(booking_id=booking_id)
    return redirect(url_for('booking_list', date=date))


@app.route('/update-list')
def update_date():
    return redirect(url_for('booking_list'))


@app.route('/confirm-booking', methods=['get', 'post'])
def confirm_booking():
    booking_list = utils.load_booking_list_query()
    return render_template('nurse/confirm_register.html', booking_list=booking_list, count_register=utils.count_register_in_query())


@app.route('/accept-booking')
def accept_booking():
    booking_id = request.args.get('booking_id')
    date = utils.get_date_by_booking_id(booking_id=booking_id)
    if (utils.count_list(date) < utils.max_patient(date)):
        utils.comfirm_booking(booking_id=booking_id)
        utils.add_user_in_register(user_id=session.get('_user_id'), register_id=booking_id)
    else:
        utils.delete_booking(booking_id=booking_id)
        err_msg = 'Danh sách ngày chọn khám đã đầy'
        return redirect(url_for('confirm_booking', err_msg=err_msg))
    err_msg= 'Xác nhận thành công'
    return redirect(url_for('confirm_booking', err_msq=err_msg))


@app.route('/reject-booking')
def reject_booking():
    booking_id = request.args.get('booking_id')
    utils.delete_booking(booking_id=booking_id)
    return redirect(url_for('confirm_booking'))


@app.route('/confirm_tested')
def confirm_tested():
    booking_id = request.args.get('booking_id')
    utils.confirm_tested(booking_id=booking_id)
    return render_template('doctor/testinglist.html')


@app.route('/testing-list')
def testing_list():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    testing_list = utils.load_testing_list(doctor_id=session.get('_user_id'), date=date)
    return render_template('doctor/testinglist.html',testing_list=testing_list, date=date)


@app.route('/add_prescription', methods=['get', 'post'])
def add_prescription():
    booking_id = request.args.get('booking_id')
    phieu_id = utils.add_phieu_kham_benh(booking_id=booking_id)
    booking = utils.get_booking_by_id(request.args.get('booking_id'))
    phieu = utils.get_phieu_benh_by_phieu_dk(booking_id)
    return render_template('doctor/test_results.html', phieu=phieu, booking=booking, booking_id=booking_id, phieu_id=phieu_id)


@app.route('/test-results', methods=['get', 'post'])
def test_results():
    booking_id = request.args.get('booking_id')
    phieu_id = request.args.get('phieu_id')
    trieu_chung = request.args.get('trieu_chung')
    benh = request.args.get('benh')
    utils.update_phieu_kham_benh(phieukham_id=booking_id, trieuchung=trieu_chung, dudoanbenh=benh)
    booking = utils.get_booking_by_id(booking_id)
    prescription = utils.load_drugs_in_precription(precription_id=phieu_id)
    phieu = utils.get_phieu_benh_by_phieu_dk(booking_id)
    return render_template('doctor/test_results.html', booking=booking, booking_id=booking_id, phieu=phieu, phieu_id=phieu_id, prescription=prescription)


@app.route('/test-results/prescription', methods=['get', 'post'])
def prescription():
    phieu_id = request.args.get('phieu_id')
    booking_id = request.args.get('booking_id')
    drugs = utils.load_drugs()
    return render_template('doctor/prescription.html', drugs=drugs, booking_id=booking_id, phieu_id=phieu_id)


@app.route('/test-results/add_drug_in_precription', methods=['get', 'post'])
def add_drug_in_precription():
    phieu_id = request.args.get('phieu_id')
    booking_id = request.args.get('booking_id')
    booking = utils.get_booking_by_id(booking_id)
    phieu = utils.get_phieu_benh_by_phieu_dk(booking.id)
    drug_id = request.args.get('drug_id')
    cachdung = request.args.get('cachdung')
    soluongthuoc = request.args.get('soluong')
    utils.add_phieu_kham_benh_thuoc(thuoc_id=drug_id, phieukhambenh_id=phieu_id, soluongthuoc=soluongthuoc, cachdung=cachdung)
    prescription = utils.load_drugs_in_precription(precription_id=phieu_id)
    return render_template('doctor/test_results.html', booking=booking, booking_id=booking_id, phieu=phieu, drugs=drug_id, phieu_id=phieu_id, prescription =prescription)


@app.route('/test-results/delete-drugs-in-prescription')
def delete_drugs_in_prescription():
    booking_id = request.args.get('booking_id')
    booking = utils.get_booking_by_id(request.args.get('booking_id'))
    drugs = utils.load_drugs()
    phieu = utils.get_phieu_benh_by_phieu_dk(booking.id)
    phieu_id = request.args.get('phieu_id')
    thuoc_id = request.args.get('thuoc_id')
    utils.delete_drugs_in_prescription(phieukham_id=phieu_id, thuoc_id=thuoc_id)
    prescription = utils.load_drugs_in_precription(precription_id=phieu_id)
    return render_template('doctor/test_results.html', booking=booking, phieu=phieu, booking_id=booking_id, drugs=drugs, phieu_id=phieu_id, prescription=prescription)


# Khi bác sĩ nhấn nút xác nhập tại lập phiếu khám bệnh, tested ở phiếu đăng kí khám sẽ bật lên true, phiếu sẽ loại khỏi
# hàng chờ đợi khám
@app.route('/tested-booking')
def tested_booking():
    booking_id = request.args.get('booking_id')
    utils.check_tested(booking_id)
    date=request.form.get('date')
    testing_list = utils.load_testing_list(doctor_id=session.get('_user_id'), date=date)
    return render_template('doctor/testinglist.html', testing_list = testing_list)


@app.route('/bill', methods=['get', 'post'])
def bill():
    flag=True;
    booking_list = utils.load_bill()
    return render_template('nurse/confirm_register.html', booking_list=booking_list,
                           count_register=utils.count_register_in_query(), flag=flag)


@app.route('/thanh-toan', methods=['get', 'post'])
def thanh_toan():
    booking = utils.get_booking_by_id(request.args.get('booking_id'))
    tien_kham = utils.get_tien_kham()
    tong_thuoc = utils.drugs_total(booking.id)
    tong_tien = tong_thuoc+tien_kham
    return render_template('nurse/bill.html', booking=booking, tien_kham=tien_kham, tong_thuoc=tong_thuoc, tong_tien=tong_tien)


@app.route('/add_hoa_don', methods=['get', 'post'])
def add_hoa_don():
    booking_id = request.args.get('booking_id')
    tien_kham = request.args.get('tien_kham')
    tong_thuoc = request.args.get('tong_thuoc')
    tong_tien = request.args.get('tong_tien')
    utils.create_hoa_don(tien_kham=tien_kham, tong_thuoc=tong_thuoc, tong_tien=tong_tien, booking_id=booking_id, user_id=session.get('_user_id'))
    booking_list = utils.load_bill()
    return render_template('nurse/confirm_register.html', booking_list=booking_list,
                           count_register=utils.count_register_in_query(), flag=True)


@app.context_processor
def common_response():
    return {
        'count_register': utils.count_register_in_query(),
        'count_bill': utils.count_bill_in_query()
    }


if __name__ == '__main__':
    from BTL.admin import *

    app.run(debug=True)
