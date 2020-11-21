CREATE DATABASE sisanf202014;
CREATE TABLE `empresa_sobrenombre` (
  `idSobreNombre` int NOT NULL AUTO_INCREMENT,
  `sobreNombre` varchar(100) NOT NULL,
  PRIMARY KEY (`idSobreNombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `estados_balance` (
  `idBalance` int NOT NULL AUTO_INCREMENT,
  `fechaInicioBalance` date NOT NULL,
  `fechaFinBalance` date NOT NULL,
  `yearEstado` smallint unsigned NOT NULL,
  `moneda_balance` varchar(40) NOT NULL,
  `moneda_codigo_balance` varchar(3) NOT NULL,
  PRIMARY KEY (`idBalance`),
  CONSTRAINT `estados_balance_chk_1` CHECK ((`yearEstado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `estados_estadoderesultado` (
  `idResultado` int NOT NULL AUTO_INCREMENT,
  `fechaInicioEstado` date NOT NULL,
  `fechaFinEstado` date NOT NULL,
  `yearEstado` smallint unsigned NOT NULL,
  `moneda_estado` varchar(40) NOT NULL,
  `moneda_codigo_estado` varchar(3) NOT NULL,
  PRIMARY KEY (`idResultado`),
  CONSTRAINT `estados_estadoderesultado_chk_1` CHECK ((`yearEstado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `giro_giro` (
  `idGiro` int unsigned NOT NULL,
  `nombreGiro` varchar(100) NOT NULL,
  `sector` varchar(2) NOT NULL,
  PRIMARY KEY (`idGiro`),
  CONSTRAINT `giro_giro_chk_1` CHECK ((`idGiro` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `giro_ratios` (
  `idRatio` int unsigned NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `nomRatio` varchar(50) NOT NULL,
  PRIMARY KEY (`idRatio`),
  CONSTRAINT `giro_ratios_chk_1` CHECK ((`idRatio` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `usuarios_opcionform` (
  `idOpcion` varchar(3) NOT NULL,
  `descOpcion` varchar(100) NOT NULL,
  `numForm` int unsigned NOT NULL,
  PRIMARY KEY (`idOpcion`),
  UNIQUE KEY `Usuarios_opcionform_idOpcion_descOpcion_numForm_22871cc4_uniq` (`idOpcion`,`descOpcion`,`numForm`),
  CONSTRAINT `usuarios_opcionform_chk_1` CHECK ((`numForm` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `usuarios_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `id` varchar(2) NOT NULL,
  `nomUsuario` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `rol` smallint NOT NULL,
  `is_administrador` tinyint(1) NOT NULL,
  `is_analista` tinyint(1) NOT NULL,
  `is_gerente` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nomUsuario` (`nomUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `empresa_empresa` (
  `idEmpresa` int NOT NULL AUTO_INCREMENT,
  `rasonsocial` varchar(50) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `nrc` varchar(8) NOT NULL,
  `nit` varchar(17) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `gerente_id` varchar(2) NOT NULL,
  `idGiro_id` int unsigned NOT NULL,
  PRIMARY KEY (`idEmpresa`),
  UNIQUE KEY `gerente_id` (`gerente_id`),
  KEY `Empresa_empresa_idGiro_id_8f2f28ad_fk_Giro_giro_idGiro` (`idGiro_id`),
  CONSTRAINT `Empresa_empresa_gerente_id_c4acf4b5_fk_Usuarios_user_id` FOREIGN KEY (`gerente_id`) REFERENCES `usuarios_user` (`id`),
  CONSTRAINT `Empresa_empresa_idGiro_id_8f2f28ad_fk_Giro_giro_idGiro` FOREIGN KEY (`idGiro_id`) REFERENCES `giro_giro` (`idGiro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `analisis_analisis` (
  `idAnalisis` int NOT NULL AUTO_INCREMENT,
  `year_analisis` smallint unsigned NOT NULL,
  `year_previos` smallint unsigned NOT NULL,
  `conclusion_horizontal` longtext,
  `conclusion_vertical` longtext,
  `idEmpresa_id` int NOT NULL,
  PRIMARY KEY (`idAnalisis`),
  KEY `Analisis_analisis_idEmpresa_id_2969bf20_fk_Empresa_e` (`idEmpresa_id`),
  CONSTRAINT `Analisis_analisis_idEmpresa_id_2969bf20_fk_Empresa_e` FOREIGN KEY (`idEmpresa_id`) REFERENCES `empresa_empresa` (`idEmpresa`),
  CONSTRAINT `analisis_analisis_chk_1` CHECK ((`year_analisis` >= 0)),
  CONSTRAINT `analisis_analisis_chk_2` CHECK ((`year_previos` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `analisis_balanceanalisis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idAnalisis_id` int NOT NULL,
  `idbalance_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Analisis_balanceanal_idAnalisis_id_fc4c400e_fk_Analisis_` (`idAnalisis_id`),
  KEY `Analisis_balanceanal_idbalance_id_85a5da7c_fk_Estados_b` (`idbalance_id`),
  CONSTRAINT `Analisis_balanceanal_idAnalisis_id_fc4c400e_fk_Analisis_` FOREIGN KEY (`idAnalisis_id`) REFERENCES `analisis_analisis` (`idAnalisis`),
  CONSTRAINT `Analisis_balanceanal_idbalance_id_85a5da7c_fk_Estados_b` FOREIGN KEY (`idbalance_id`) REFERENCES `estados_balance` (`idBalance`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `analisis_estadoanalisis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idAnalisis_id` int NOT NULL,
  `idResultado_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Analisis_estadoanali_idAnalisis_id_b14bd949_fk_Analisis_` (`idAnalisis_id`),
  KEY `Analisis_estadoanali_idResultado_id_1512c9b0_fk_Estados_e` (`idResultado_id`),
  CONSTRAINT `Analisis_estadoanali_idAnalisis_id_b14bd949_fk_Analisis_` FOREIGN KEY (`idAnalisis_id`) REFERENCES `analisis_analisis` (`idAnalisis`),
  CONSTRAINT `Analisis_estadoanali_idResultado_id_1512c9b0_fk_Estados_e` FOREIGN KEY (`idResultado_id`) REFERENCES `estados_estadoderesultado` (`idResultado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `empresa_cuenta` (
  `idCuenta` int NOT NULL AUTO_INCREMENT,
  `codigo_cuenta` varchar(13) NOT NULL,
  `nombre_cuenta` varchar(100) NOT NULL,
  `tipo_cuenta` varchar(25) DEFAULT NULL,
  `naturaleza_cuenta` varchar(12) DEFAULT NULL,
  `idEmpresa_id` int NOT NULL,
  `idSobreNombre_id` int DEFAULT NULL,
  PRIMARY KEY (`idCuenta`),
  KEY `Empresa_cuenta_idEmpresa_id_0f927246_fk_Empresa_e` (`idEmpresa_id`),
  KEY `Empresa_cuenta_idSobreNombre_id_80f4238b_fk_Empresa_s` (`idSobreNombre_id`),
  CONSTRAINT `Empresa_cuenta_idEmpresa_id_0f927246_fk_Empresa_e` FOREIGN KEY (`idEmpresa_id`) REFERENCES `empresa_empresa` (`idEmpresa`),
  CONSTRAINT `Empresa_cuenta_idSobreNombre_id_80f4238b_fk_Empresa_s` FOREIGN KEY (`idSobreNombre_id`) REFERENCES `empresa_sobrenombre` (`idSobreNombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `analisis_lineadeinforme` (
  `idLineaInfo` int NOT NULL AUTO_INCREMENT,
  `variacion_horizontal` decimal(12,2) NOT NULL,
  `porcentaje_horizontal` decimal(7,4) NOT NULL,
  `porcentaje_vertical` decimal(7,4) DEFAULT NULL,
  `idAnalisis_id` int NOT NULL,
  `idCuenta_id` int NOT NULL,
  PRIMARY KEY (`idLineaInfo`),
  KEY `Analisis_lineadeinfo_idAnalisis_id_c5807d41_fk_Analisis_` (`idAnalisis_id`),
  KEY `Analisis_lineadeinfo_idCuenta_id_993916d0_fk_Empresa_c` (`idCuenta_id`),
  CONSTRAINT `Analisis_lineadeinfo_idAnalisis_id_c5807d41_fk_Analisis_` FOREIGN KEY (`idAnalisis_id`) REFERENCES `analisis_analisis` (`idAnalisis`),
  CONSTRAINT `Analisis_lineadeinfo_idCuenta_id_993916d0_fk_Empresa_c` FOREIGN KEY (`idCuenta_id`) REFERENCES `empresa_cuenta` (`idCuenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `analisis_ratiosanalisis` (
  `idRatioAnalisis` int NOT NULL AUTO_INCREMENT,
  `valorRatiosAnalisis` decimal(8,4) NOT NULL,
  `conclusion` longtext,
  `idAnalisis_id` int NOT NULL,
  `idRatios_id` int unsigned NOT NULL,
  PRIMARY KEY (`idRatioAnalisis`),
  KEY `Analisis_ratiosanali_idAnalisis_id_d8440b93_fk_Analisis_` (`idAnalisis_id`),
  KEY `Analisis_ratiosanali_idRatios_id_b3c4899f_fk_Giro_rati` (`idRatios_id`),
  CONSTRAINT `Analisis_ratiosanali_idAnalisis_id_d8440b93_fk_Analisis_` FOREIGN KEY (`idAnalisis_id`) REFERENCES `analisis_analisis` (`idAnalisis`),
  CONSTRAINT `Analisis_ratiosanali_idRatios_id_b3c4899f_fk_Giro_rati` FOREIGN KEY (`idRatios_id`) REFERENCES `giro_ratios` (`idRatio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` varchar(2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Usuarios_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Usuarios_user_id` FOREIGN KEY (`user_id`) REFERENCES `usuarios_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `empresa_balanceempresa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idEmpresa_id` int NOT NULL,
  `idbalance_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Empresa_balanceempre_idEmpresa_id_801e0a4d_fk_Empresa_e` (`idEmpresa_id`),
  KEY `Empresa_balanceempre_idbalance_id_524f5f15_fk_Estados_b` (`idbalance_id`),
  CONSTRAINT `Empresa_balanceempre_idbalance_id_524f5f15_fk_Estados_b` FOREIGN KEY (`idbalance_id`) REFERENCES `estados_balance` (`idBalance`),
  CONSTRAINT `Empresa_balanceempre_idEmpresa_id_801e0a4d_fk_Empresa_e` FOREIGN KEY (`idEmpresa_id`) REFERENCES `empresa_empresa` (`idEmpresa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `empresa_estadoempresa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idEmpresa_id` int NOT NULL,
  `idResultado_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Empresa_estadoempres_idEmpresa_id_204516d8_fk_Empresa_e` (`idEmpresa_id`),
  KEY `Empresa_estadoempres_idResultado_id_5c80fa5b_fk_Estados_e` (`idResultado_id`),
  CONSTRAINT `Empresa_estadoempres_idEmpresa_id_204516d8_fk_Empresa_e` FOREIGN KEY (`idEmpresa_id`) REFERENCES `empresa_empresa` (`idEmpresa`),
  CONSTRAINT `Empresa_estadoempres_idResultado_id_5c80fa5b_fk_Estados_e` FOREIGN KEY (`idResultado_id`) REFERENCES `estados_estadoderesultado` (`idResultado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `empresa_saldodecuentabalace` (
  `idSaldo` int NOT NULL AUTO_INCREMENT,
  `year_saldo` date NOT NULL,
  `monto_saldo` decimal(11,2) NOT NULL,
  `idCuenta_id` int NOT NULL,
  `idbalance_id` int NOT NULL,
  PRIMARY KEY (`idSaldo`),
  KEY `Empresa_saldodecuent_idCuenta_id_332579d7_fk_Empresa_c` (`idCuenta_id`),
  KEY `Empresa_saldodecuent_idbalance_id_6d750540_fk_Estados_b` (`idbalance_id`),
  CONSTRAINT `Empresa_saldodecuent_idbalance_id_6d750540_fk_Estados_b` FOREIGN KEY (`idbalance_id`) REFERENCES `estados_balance` (`idBalance`),
  CONSTRAINT `Empresa_saldodecuent_idCuenta_id_332579d7_fk_Empresa_c` FOREIGN KEY (`idCuenta_id`) REFERENCES `empresa_cuenta` (`idCuenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `empresa_saldodecuentaresultado` (
  `idSaldoResul` int NOT NULL AUTO_INCREMENT,
  `year_saldo_Resul` date NOT NULL,
  `monto_saldo_Resul` decimal(11,2) NOT NULL,
  `idCuenta_id` int NOT NULL,
  `idResultado_id` int NOT NULL,
  PRIMARY KEY (`idSaldoResul`),
  KEY `Empresa_saldodecuent_idCuenta_id_8cfb09be_fk_Empresa_c` (`idCuenta_id`),
  KEY `Empresa_saldodecuent_idResultado_id_9582e9bc_fk_Estados_e` (`idResultado_id`),
  CONSTRAINT `Empresa_saldodecuent_idCuenta_id_8cfb09be_fk_Empresa_c` FOREIGN KEY (`idCuenta_id`) REFERENCES `empresa_cuenta` (`idCuenta`),
  CONSTRAINT `Empresa_saldodecuent_idResultado_id_9582e9bc_fk_Estados_e` FOREIGN KEY (`idResultado_id`) REFERENCES `estados_estadoderesultado` (`idResultado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `giro_datogiro` (
  `idDato` int NOT NULL AUTO_INCREMENT,
  `valorParametro` double NOT NULL,
  `valorPromedio` double NOT NULL,
  `idGiro_id` int unsigned NOT NULL,
  `idRatio_id` int unsigned NOT NULL,
  PRIMARY KEY (`idDato`),
  UNIQUE KEY `Giro_datogiro_idGiro_id_idRatio_id_ebbc625f_uniq` (`idGiro_id`,`idRatio_id`),
  KEY `Giro_datogiro_idRatio_id_c31a3fae_fk_Giro_ratios_idRatio` (`idRatio_id`),
  CONSTRAINT `Giro_datogiro_idGiro_id_de7dc46d_fk_Giro_giro_idGiro` FOREIGN KEY (`idGiro_id`) REFERENCES `giro_giro` (`idGiro`),
  CONSTRAINT `Giro_datogiro_idRatio_id_c31a3fae_fk_Giro_ratios_idRatio` FOREIGN KEY (`idRatio_id`) REFERENCES `giro_ratios` (`idRatio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `usuarios_accesousuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idOpcion_id` varchar(3) NOT NULL,
  `idUsuario_id` varchar(2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Usuarios_accesousuario_idUsuario_id_idOpcion_id_be360a51_uniq` (`idUsuario_id`,`idOpcion_id`),
  KEY `Usuarios_accesousuar_idOpcion_id_8ad08ba1_fk_Usuarios_` (`idOpcion_id`),
  CONSTRAINT `Usuarios_accesousuar_idOpcion_id_8ad08ba1_fk_Usuarios_` FOREIGN KEY (`idOpcion_id`) REFERENCES `usuarios_opcionform` (`idOpcion`),
  CONSTRAINT `Usuarios_accesousuario_idUsuario_id_2a8f6a1f_fk_Usuarios_user_id` FOREIGN KEY (`idUsuario_id`) REFERENCES `usuarios_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
