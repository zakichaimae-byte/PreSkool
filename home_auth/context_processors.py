def translations(request):
    lang = getattr(request, 'LANGUAGE_CODE', 'fr')
    
    # Dictionnaire de traductions pour les éléments de l'interface
    translations_dict = {
        'fr': {
            'menu_principal': 'Menu Principal',
            'dashboard_label': 'Tableau de bord',
            'administration': 'Administration',
            'txt_students': 'Étudiants',
            'txt_teachers': 'Enseignants',
            'txt_departments': 'Départements',
            'txt_subjects': 'Matières',
            'academic_management': 'Gestion Académique',
            'settings': 'Paramètres',
            'logout': 'Déconnexion',
            'welcome_to': 'Bienvenue sur',
            'dashboard_subtitle': 'Tableau de bord de gestion scolaire intelligent et moderne.',
            'gender_distribution': 'Répartition par Genre',
            'boys': 'Garçons',
            'girls': 'Filles',
        },
        'en': {
            'menu_principal': 'Main Menu',
            'dashboard_label': 'Dashboard',
            'administration': 'Administration',
            'txt_students': 'Students',
            'txt_teachers': 'Teachers',
            'txt_departments': 'Departments',
            'txt_subjects': 'Subjects',
            'academic_management': 'Academic Management',
            'settings': 'Settings',
            'logout': 'Logout',
            'welcome_to': 'Welcome to',
            'dashboard_subtitle': 'Modern and smart school management dashboard.',
            'gender_distribution': 'Gender Distribution',
            'boys': 'Boys',
            'girls': 'Girls',
        },
        'ar': {
            'menu_principal': 'القائمة الرئيسية',
            'dashboard_label': 'لوحة التحكم',
            'administration': 'الإدارة',
            'txt_students': 'الطلاب',
            'txt_teachers': 'المعلمون',
            'txt_departments': 'الأقسام',
            'txt_subjects': 'المواد',
            'academic_management': 'الإدارة الأكاديمية',
            'settings': 'الإعدادات',
            'logout': 'تسجيل الخروج',
            'welcome_to': 'مرحباً بك في',
            'dashboard_subtitle': 'لوحة تحكم ذكية وحديثة لإدارة المدرسة.',
            'gender_distribution': 'توزيع الجنس',
            'boys': 'أولاد',
            'girls': 'بنات',
        }
    }
    
    # On récupère les traductions pour la langue actuelle (fr par défaut)
    return translations_dict.get(lang[:2], translations_dict['fr'])
