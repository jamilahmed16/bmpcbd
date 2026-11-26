<?php
/** BMPC header (replaces Divi's header). */
if ( ! defined( 'ABSPATH' ) ) { exit; }
$logo = BMPC_URI . '/assets/img/logo-192.webp'; // 14 KB; the 512 px media-library logo is for the site icon
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div id="page-container">
<header class="top" id="top-header-bmpc"><div class="wrap">
	<a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল, হোম">
		<img class="logo" src="<?php echo esc_url( $logo ); ?>" width="68" height="68" alt="" fetchpriority="high">
		<span><b>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</b></span>
	</a>
	<nav class="nav" aria-label="প্রধান মেনু">
		<?php wp_nav_menu( array( 'theme_location' => 'primary-menu', 'container' => false, 'menu_class' => 'bmpc-menu', 'depth' => 2, 'fallback_cb' => 'bmpc_fallback_menu' ) ); ?>
	</nav>
	<a class="btn btn-paper" href="<?php echo esc_url( bmpc_page_url( 'join' ) ); ?>">সদস্য হোন</a>
	<details class="menu"><summary>মেনু</summary><nav class="drop" aria-label="মোবাইল মেনু">
		<?php wp_nav_menu( array( 'theme_location' => 'primary-menu', 'container' => false, 'menu_class' => 'bmpc-mmenu', 'depth' => 2, 'fallback_cb' => 'bmpc_fallback_menu' ) ); ?>
		<a class="drop-join" href="<?php echo esc_url( bmpc_page_url( 'join' ) ); ?>">সদস্য হোন</a>
	</nav></details>
</div></header>
<div id="et-main-area">
<?php if ( bmpc_wraps_main() ) { echo '<main id="main">'; } ?>
