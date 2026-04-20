from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
     path('', views.login_view, name="login"),
     path(
         'password-reset/',
         views.UsernamePasswordResetView.as_view(
             success_url=reverse_lazy('password_reset_done'),
         ),
         name='password_reset',
     ),
     path(
         'password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password_reset_done.html',
         ),
         name='password_reset_done',
     ),
     path(
         'reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete'),
         ),
         name='password_reset_confirm',
     ),
     path(
         'reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password_reset_complete.html',
         ),
         name='password_reset_complete',
     ),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('create-lead/', views.create_lead, name='create_lead'),         
     path('create-user/', views.create_user, name="create_user"),

     #department 
     path('department/', views.department_view, name='department'),
     path('department/delete/<int:pk>/', views.delete_department, name='delete_department'),

     #course
     path('course/', views.course_view, name='course'),
     path('course/delete/<int:pk>/', views.delete_course, name='delete_course'),
     path('course/', views.course_view, name='course'),
     path('course/edit/', views.edit_course, name='edit_course'),
     path('course/delete/<int:pk>/', views.delete_course, name='delete_course'),
     
     path('bulk-update-status/', views.bulk_update_status, name='bulk_update_status'),
     path('bulk-delete-leads/', views.bulk_delete_leads, name='bulk_delete_leads'),
     path('bulk-assign-leads/', views.bulk_assign_leads, name='bulk_assign_leads'),

     path('leads/<int:lead_id>/', views.lead_profile, name='lead_profile'),
     path("leads/<int:lead_id>/add-task/",views.add_task,name="add_task"),



     path("attendance/<int:batch_id>/", views.mark_attendance, name="mark_attendance"),
     path("attendance/view/", views.view_attendance, name="view_attendance"),
     path("attendance/monthly/", views.monthly_attendance_view, name="monthly_attendance_view"),
     path("attendance/trainers/", views.trainer_attendance_report, name="trainer_attendance_report"),



     path('exams/', views.exam_list, name='exam_list'),
     path('exams/<int:exam_id>/', views.exam_detail, name='exam_detail'),
     path('exams/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),
     path('exams/<int:exam_id>/question-paper/', views.question_paper, name='question_paper'),
     path('exams/<int:exam_id>/question-paper/download/', views.download_question_paper, name='download_question_paper'),
     

     path('students/bulk-status/', views.bulk_update_student_status,
          name='bulk_update_student_status'),
     path('students/bulk-delete/', views.bulk_delete_students,
          name='bulk_delete_students'),
     path('assign-batch/', views.assign_students_batch, name='assign_students_batch'),
     path('get-batch-students/<int:batch_id>/', views.get_batch_students, name='get_batch_students'),
     path('assign-single-student-batch/', views.assign_single_student_batch, name='assign_single_student_batch'),
     path('remove-student-batch/', views.remove_student_batch, name='remove_student_batch'),
     path('assign-multiple-students-batch/', views.assign_multiple_students_batch, name='assign_multiple_students_batch'),
     path('remove-multiple-students-batch/', views.remove_multiple_students_batch, name='remove_multiple_students_batch'),
     path('batch/<int:batch_id>/students/', views.batch_students, name='batch_students'),

    path('syllabus/', views.syllabus_view, name='syllabus'),
    path('syllabus/add-module/', views.add_module, name='add_module'),
    path('syllabus/edit-module/', views.edit_module, name='edit_module'),
    path('syllabus/delete-module/<int:pk>/', views.delete_module, name='delete_module'),
    path('syllabus/add-topics/', views.add_topics, name='add_topics'),
    path('syllabus/edit-topic/', views.edit_topic, name='edit_topic'),
    path('syllabus/delete-topic/<int:pk>/', views.delete_topic, name='delete_topic'),
    path('syllabus/trainer/', views.trainer_syllabus, name='trainer_syllabus'),

    #payment
    path('payments/', views.payments, name='payments'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/add/<int:fee_id>/', views.add_payment, name='add_payment_for_fee'),
    path('payments/undo/<int:payment_id>/', views.undo_payment, name='undo_payment'),
    path('mail-management/', views.mail_management, name='mail_management'),
    path('mail-management/pending/', views.mail_pending_list, name='mail_pending_list'),
    path('mail-management/pending/payment-confirmation/', views.payment_email_pending_list, name='payment_email_pending_list'),
    path('mail-management/pending/overdue/', views.overdue_email_pending_list, name='overdue_email_pending_list'),
    path('mail-management/pending/preview-batch/<int:pending_id>/', views.preview_batch_pending_mail_action, name='preview_batch_pending_mail_action'),
    path('mail-management/pending/preview-payment/<int:pending_id>/', views.preview_payment_pending_mail_action, name='preview_payment_pending_mail_action'),
    path('mail-management/pending/preview-overdue/<int:pending_id>/', views.preview_overdue_pending_mail_action, name='preview_overdue_pending_mail_action'),
    path('mail-management/logs/preview/<int:log_id>/', views.preview_mail_log_action, name='preview_mail_log_action'),
    path('mail-management/send/<int:pending_id>/', views.send_pending_mail_action, name='send_pending_mail_action'),
    path('mail-management/send-bulk/', views.send_bulk_pending_mail_action, name='send_bulk_pending_mail_action'),
    path('mail-management/send-bulk/payment/', views.send_bulk_payment_pending_mail_action, name='send_bulk_payment_pending_mail_action'),
    path('mail-management/send-bulk/overdue/', views.send_bulk_overdue_pending_mail_action, name='send_bulk_overdue_pending_mail_action'),
    path('invoices/', views.invoice_view, name='invoice_view'),
    path('invoices/<int:fee_id>/', views.invoice_view, name='invoice_view_detail'),


     path("session-update/", views.session_update, name="session_update"),
     path("get-batch-topics/", views.get_batch_topics, name="get_batch_topics"),
     path("session-updates/", views.session_update_list, name="session_update_list"),
     path("session-updates/<int:session_id>/edit/", views.edit_session_update, name="edit_session_update"),
     path("session-updates/<int:session_id>/delete/", views.delete_session_update, name="delete_session_update"),
     
     # Assignment tracking
     path('assignments/', views.assignment_list, name='assignment_list'),
     path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
     path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

     # Reports
     path('reports/leads/', views.lead_report, name='lead_report'),
     path('reports/leads/export/', views.lead_report_export, name='lead_report_export'),
     path('reports/students/', views.student_report, name='student_report'),
     path('reports/students/export/', views.student_report_export, name='student_report_export'),
     path('reports/courses/', views.course_report, name='course_report'),
     path('reports/courses/export/', views.course_report_export, name='course_report_export'),
     path('reports/batches/', views.batch_report, name='batch_report'),
     path('reports/batches/export/', views.batch_report_export, name='batch_report_export'),
     path('reports/assignments/', views.assignment_report, name='assignment_report'),
     path('reports/assignments/export/', views.assignment_report_export, name='assignment_report_export'),
     path('reports/payments/', views.payment_report, name='payment_report'),
     path('reports/payments/export/', views.payment_report_export, name='payment_report_export'),
     path('reports/students/<int:student_id>/', views.student_individual_report, name='student_individual_report'),
     path('reports/students/<int:student_id>/send-email/', views.send_student_report_email, name='send_student_report_email'),

     path('reports/exams/', views.exam_report, name='exam_report'),
     path('reports/exams/export/', views.exam_report_export, name='exam_report_export'),

    path('leads/filter/', views.leads__filter, name='leads_filter'),

    path('status/', views.status_view, name="status"),  
    path('source/', views.source_view, name='source'),
    path('leads/edit/<int:lead_id>/', views.edit_lead, name='edit_lead'),
    path('leads/delete/<int:lead_id>/', views.delete_lead, name='delete_lead'),
    path('leads/update-status/<int:lead_id>/', views.update_lead_status, name='update_lead_status'),
    path('leads/update-type/<int:lead_id>/', views.update_lead_type, name='update_lead_type'),
    path('status/delete/<int:pk>/', views.delete_status, name='delete_status'),
    path('source/delete/<int:pk>/', views.delete_source, name='delete_source'),
    path('ajax/get-courses/', views.get_courses_by_department, name='get_courses_by_department'),
    path('ajax/get-modules/', views.get_modules_by_course, name='get_modules_by_course'),


     path('leads/import-excel/', views.import_leads_excel, name='import_leads_excel'),
    path('leads/', views.leads__filter, name='leads'),
    path('followups/', views.followups, name='followups'),
    path('followups/complete/<int:followup_id>/', views.complete_followup, name='complete_followup'),
    path('followups/cancel/<int:followup_id>/', views.cancel_followup, name='cancel_followup'),
    path('followups/undo/<int:followup_id>/', views.undo_followup, name='undo_followup'),
    path('followups/add/<int:lead_id>/', views.add_followup, name='add_followup'),
    path('followups/live-search/', views.followup_live_search, name='followup_live_search'),
    path('leads/detail/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('leads/live-search/', views.lead_live_search, name='lead_live_search'),
    

    


    path('students/', views.students_list, name='students'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/view/<int:student_id>/', views.student_view, name='student_view'),
    path('fees/<int:fee_id>/customize-installments/', views.customize_fee_installments, name='customize_fee_installments'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path("students/", views.students_list, name="students"),
    path("students/edit/<int:id>/", views.student_edit, name="student_edit"),
    path('students/live-search/', views.student_live_search, name='student_live_search'),


    path('logout/', views.logout_view, name="logout"),


    path('cre-dashboard/', views.cre_dashboard, name="cre_dashboard"),
 

    # User management
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/live-search/', views.user_live_search, name='user_live_search'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    
    path('batch/', views.batch_view, name='batch'),
    path('batch/add/', views.add_batch, name='add_batch'),
    path('batch/edit/<int:batch_id>/', views.edit_batch, name='edit_batch'),
    path('batch/delete/<int:batch_id>/', views.delete_batch, name='delete_batch'),
    path('batch/<int:batch_id>/students/', views.batch_students, name='batch_students'),
    path('api/get-eligible-trainers/', views.get_eligible_trainers, name='get_eligible_trainers'),

    
    # CRE URLs
    path('cre/dashboard/', views.cre_dashboard, name='cre_dashboard'),
    path('cre/leads/', views.cre_leads, name='cre_leads'),
    path('cre/create-lead/', views.cre_create_lead, name='cre_create_lead'),
    path('cre/followups/', views.cre_followups, name='cre_followups'),
    
    # Notifications
    path('api/trainer-notifications/', views.get_trainer_notifications, name='trainer_notifications'),
    path('api/notifications/dismiss/', views.dismiss_notification, name='dismiss_notification'),
    
    # Global Search
    path('api/search/', views.global_search, name='api_global_search'),
]
