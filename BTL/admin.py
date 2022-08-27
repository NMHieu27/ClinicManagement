from BTL import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from BTL.models import User, DanhSachDangKiKham, Thuoc, UserRole, Rules
from flask_login import current_user, logout_user
from flask import redirect, request
from datetime import datetime
import utils


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class UserView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_exclude_list = ['avatar', 'password']
    column_filters = ['name', 'username', 'phonenumber', 'sex', 'address', 'user_role', 'joined_date', 'yearofbirth']
    column_searchable_list = ['name', 'username', 'phonenumber', 'sex', 'address', 'user_role', 'joined_date', 'yearofbirth']
    column_labels = {
        'name': 'Tên',
        'sex': 'Giới tính',
        'yearofbirth': 'Năm sinh',
        'address': 'Địa chỉ',
        'phonenumber': 'Số điện thoại',
        'joined_date': 'Ngày đăng kí',
        'user_role': 'Vai trò',
        'avatar': 'Ảnh đại diện'
    }


class DanhSachDangKiKhamView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_filters = ['max_benhnhan', 'ngaykham']
    column_searchable_list = ['max_benhnhan', 'ngaykham']
    column_labels = {
        'max_benhnhan': 'Số lượng bệnh nhân tối đa',
        'ngaykham': 'Ngày khám'
    }


class ThuocView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_filters = ['name', 'description', 'donvi', 'gia']
    column_searchable_list = ['name', 'description', 'donvi', 'gia']
    column_labels = {
        'name': 'Tên thuốc',
        'description': 'Mô tả',
        'donvi': 'Đơn vị thuốc',
        'gia': 'Giá'
    }


class RulesView(ModelView):
    can_view_details = True
    can_create = False
    can_export = True
    edit_modal = True
    details_modal = True
    column_filters = ['defaultbenhnhan', 'tienkham']
    column_searchable_list = ['defaultbenhnhan', 'tienkham']
    column_labels = {
        'defaultbenhnhan': 'Số bệnh nhân tối đa',
        'tienkham': 'Tiền khám'
    }


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class RevenueStats(BaseView):
    @expose('/')
    def index(self):
        month =request.args.get('month', datetime.now().month)
        return self.render('admin/revenuestats.html', month_stats=utils.revenue_month_stats(month=month),
                           total=utils.get_total_revenue_month(month=month), month=month)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class DrugStats(BaseView):
    @expose('/')
    def index(self):
        month =request.args.get('month', datetime.now().month)
        return self.render('admin/drugstats.html', drugs_month=utils.drug_month_stats(month=month), month=month)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name="Phòng khám mạch tư", template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(UserView(User, db.session, name='Quản lí user'))
admin.add_view(DanhSachDangKiKhamView(DanhSachDangKiKham, db.session, name='Cập nhật số bệnh nhân khám trong ngày'))
admin.add_view(RulesView(Rules, db.session, name='Quy định'))
admin.add_view(ThuocView(Thuoc, db.session, name='Quản lí thuốc'))
admin.add_view(RevenueStats(name='Báo cáo danh thu theo tháng'))
admin.add_view(DrugStats(name='Báo cáo sử dụng thuốc'))
admin.add_view(LogoutView(name='Logout'))