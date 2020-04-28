-- Create syntax for TABLE 'account'
CREATE TABLE `account` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned NOT NULL COMMENT 'An organization can have one or multimple account accross time. Account could be closed. Another one opened.',
  `account_number` char(32) NOT NULL COMMENT 'Possible account number (auto-generated)',
  `account_name` varchar(50) NOT NULL,
  `is_active` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'Allow track if account is active or de-activated (non payment). Inactive account cannot login.',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `timezone_name` varchar(50) NOT NULL COMMENT 'Timezone of the account.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
-- Create syntax for TABLE 'address_type'
CREATE TABLE `address_type` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `address_type_name` varchar(35) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COMMENT='Business Address,  Invoice Ship To Address,  Billing Address';
-- Create syntax for TABLE 'country'
CREATE TABLE `country` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `country_name` varchar(100) NOT NULL,
  `country_code` char(3) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_code` (`country_code`)
) ENGINE=InnoDB AUTO_INCREMENT=249 DEFAULT CHARSET=latin1;
-- Create syntax for TABLE 'country_import'
CREATE TABLE `country_import` (
  `SK_Country` int(11) DEFAULT NULL,
  `CountryName` varchar(255) DEFAULT NULL,
  `Alpha3Code` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- Create syntax for TABLE 'industry'
CREATE TABLE `industry` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `industry_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'organization_type'
CREATE TABLE `organization_type` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `organization_type_name` varchar(50) NOT NULL COMMENT 'Zappo, Supplier, Restaurant, Other (industries)',
  `is_active` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'Flag that states if ooganization type is active in the UI. (selectable)',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='Restaurant, Supplier, zappo_track, Accounting, ...';
-- Create syntax for TABLE 'restaurant'
CREATE TABLE `restaurant` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned NOT NULL,
  `restaurant_name` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
-- Create syntax for TABLE 'supplier'
CREATE TABLE `supplier` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned NOT NULL,
  `supplier_name` varchar(100) NOT NULL,
  `business_name` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `logo_path` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
-- Create syntax for TABLE 'zappo_track'
CREATE TABLE `zappo_track` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oganization_id` int(10) unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



-- Create syntax for TABLE 'address'
CREATE TABLE `address` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned NOT NULL,
  `address_type_id` tinyint(3) unsigned NOT NULL COMMENT 'Shipping, Business etc ...',
  `country_id` smallint(5) unsigned NOT NULL,
  `address_name` varchar(100) NOT NULL,
  `address_name_additional` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) NOT NULL,
  `city_name` varchar(65) NOT NULL,
  `is_active` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'Business could move to another address, address could change.',
  `from_date` date NOT NULL COMMENT 'Active Address From Date',
  `thru_date` date DEFAULT NULL COMMENT 'Active at this address till.',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'Soft delete.',
  PRIMARY KEY (`id`),
  KEY `fk_address_address_type` (`address_type_id`),
  KEY `fk_address_country` (`country_id`),
  CONSTRAINT `fk_address_address_type` FOREIGN KEY (`address_type_id`) REFERENCES `address_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_address_country` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COMMENT='Organization Address, Restaurant  Address, Invoice Ship To Address, etc ..';


-- Create syntax for TABLE 'organization'
CREATE TABLE `organization` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `parent_organization_id` int(10) unsigned DEFAULT NULL,
  `organization_type_id` smallint(5) unsigned NOT NULL COMMENT 'Zappo, Supplier, Restaurant (other industry)',
  `organization_number` varchar(32) NOT NULL DEFAULT '',
  `industry_id` smallint(5) unsigned NOT NULL,
  `organization_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `website_url` varchar(65) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `timezone_name` varchar(50) NOT NULL DEFAULT 'Pacific Daylight Time/Vancouver',
  PRIMARY KEY (`id`),
  KEY `fk_organization_organization_type` (`organization_type_id`),
  KEY `fk_organization_industry` (`industry_id`),
  KEY `idx_org_number` (`organization_number`),
  KEY `idx_parent_id` (`parent_organization_id`),
  CONSTRAINT `fk_organization_industry` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_organization_organization_type` FOREIGN KEY (`organization_type_id`) REFERENCES `organization_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
