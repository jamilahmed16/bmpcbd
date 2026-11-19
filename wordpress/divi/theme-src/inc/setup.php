<?php
/**
 * Appearance → BMPC Setup: imports images, creates pages, news posts, menu, front page and SEO meta.
 * Safe to run more than once: existing pages and posts are skipped unless "overwrite" is ticked.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'admin_menu', function () {
	add_theme_page( 'BMPC Setup', 'BMPC Setup', 'manage_options', 'bmpc-setup', 'bmpc_setup_screen' );
} );

add_action( 'after_switch_theme', function () {
	if ( ! get_option( 'bmpc_setup_done' ) ) {
		set_transient( 'bmpc_setup_notice', 1, DAY_IN_SECONDS );
	}
} );
add_action( 'admin_notices', function () {
	if ( ! get_transient( 'bmpc_setup_notice' ) || ! current_user_can( 'manage_options' ) ) { return; }
	echo '<div class="notice notice-info"><p><strong>BMPC theme activated.</strong> Open <a href="' . esc_url( admin_url( 'themes.php?page=bmpc-setup' ) ) . '">Appearance → BMPC Setup</a> to create the pages, menu and news.</p></div>';
} );

function bmpc_setup_screen() {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	$log = array();
	if ( isset( $_POST['bmpc_run'] ) && check_admin_referer( 'bmpc_setup' ) ) {
		$opt = array(
			'images'    => ! empty( $_POST['images'] ),
			'pages'     => ! empty( $_POST['pages'] ),
			'posts'     => ! empty( $_POST['posts'] ),
			'menu'      => ! empty( $_POST['menu'] ),
			'reading'   => ! empty( $_POST['reading'] ),
			'seo'       => ! empty( $_POST['seo'] ),
			'overwrite' => ! empty( $_POST['overwrite'] ),
		);
		$log = bmpc_run_setup( $opt );
		update_option( 'bmpc_setup_done', time() );
		delete_transient( 'bmpc_setup_notice' );
	}
	if ( isset( $_POST['bmpc_social_save'] ) && check_admin_referer( 'bmpc_social' ) ) {
		update_option( 'bmpc_social', array(
			'facebook'  => esc_url_raw( wp_unslash( $_POST['facebook'] ?? '' ) ),
			'x'         => esc_url_raw( wp_unslash( $_POST['x'] ?? '' ) ),
			'instagram' => esc_url_raw( wp_unslash( $_POST['instagram'] ?? '' ) ),
		) );
		$log[] = array( 'ok', 'Social links saved.' );
	}
	$s = bmpc_social();
	?>
	<div class="wrap">
		<h1>BMPC Setup</h1>
		<p>Creates the BMPC site from the design: images in the Media Library, the Divi pages, news posts, the main menu, the home page and Rank Math titles/descriptions. Pages that already exist with the same slug are <strong>left alone</strong> unless you tick “overwrite”. Back up the site before overwriting.</p>
		<?php if ( $log ) : ?>
			<div class="notice notice-success" style="padding:12px 16px"><ul style="margin:0">
			<?php foreach ( $log as $row ) : ?><li><?php echo 'ok' === $row[0] ? '✅' : ( 'skip' === $row[0] ? '⏭️' : '⚠️' ); ?> <?php echo wp_kses_post( $row[1] ); ?></li><?php endforeach; ?>
			</ul></div>
		<?php endif; ?>
		<form method="post">
			<?php wp_nonce_field( 'bmpc_setup' ); ?>
			<table class="form-table" role="presentation"><tbody>
				<tr><th>Import</th><td>
					<label><input type="checkbox" name="images" checked> Images → Media Library (logo, photos, social image)</label><br>
					<label><input type="checkbox" name="posts" checked> News posts</label><br>
					<label><input type="checkbox" name="pages" checked> Pages (হোম, আমাদের সম্পর্কে, ঘোষণাপত্র, গঠনতন্ত্র, লক্ষ্য ও উদ্দেশ্য, বাণী ×২, সদস্য হোন, সর্বশেষ সংবাদ)</label><br>
					<label><input type="checkbox" name="menu" checked> Main menu (assigned to Primary Menu)</label><br>
					<label><input type="checkbox" name="reading" checked> Settings → Reading: হোম as front page, সর্বশেষ সংবাদ as posts page</label><br>
					<label><input type="checkbox" name="seo" checked> SEO titles &amp; descriptions (Rank Math / Yoast fields)</label>
				</td></tr>
				<tr><th>Existing content</th><td><label><input type="checkbox" name="overwrite"> Overwrite pages, posts and menu that already exist (old versions stay in Revisions)</label></td></tr>
			</tbody></table>
			<p><button class="button button-primary button-hero" name="bmpc_run" value="1">Run setup</button></p>
		</form>
		<hr>
		<h2>Social links (footer icons)</h2>
		<form method="post"><?php wp_nonce_field( 'bmpc_social' ); ?>
			<table class="form-table" role="presentation"><tbody>
				<tr><th><label for="facebook">Facebook</label></th><td><input class="regular-text" id="facebook" name="facebook" value="<?php echo esc_attr( $s['facebook'] ); ?>" placeholder="https://facebook.com/…"></td></tr>
				<tr><th><label for="x">X (Twitter)</label></th><td><input class="regular-text" id="x" name="x" value="<?php echo esc_attr( $s['x'] ); ?>" placeholder="https://x.com/…"></td></tr>
				<tr><th><label for="instagram">Instagram</label></th><td><input class="regular-text" id="instagram" name="instagram" value="<?php echo esc_attr( $s['instagram'] ); ?>" placeholder="https://instagram.com/…"></td></tr>
			</tbody></table>
			<p><button class="button" name="bmpc_social_save" value="1">Save social links</button></p>
		</form>
		<hr>
		<h2>Join form</h2>
		<p>The সদস্য হোন page shows the Fluent Forms form titled “সদস্য আবেদন ফর্ম”. Import <code>bmpc-join-form.json</code> in Fluent Forms → Tools → Import first, then run setup (or re-run it with “overwrite”).</p>
	</div>
	<?php
}

function bmpc_run_setup( $opt ) {
	$data = bmpc_data();
	$log  = array();
	if ( empty( $data['pages'] ) ) { return array( array( 'warn', 'data/site.json is missing or empty.' ) ); }

	if ( $opt['images'] ) { $log = array_merge( $log, bmpc_import_images( $data['images'] ) ); }
	if ( $opt['posts'] ) {
		$log = array_merge( $log, bmpc_import_posts( $data['posts'], $opt['overwrite'], $opt['seo'] ) );
		$hello = get_page_by_path( 'hello-world', OBJECT, 'post' );
		if ( $hello && 'publish' === $hello->post_status && $hello->post_date === $hello->post_modified ) {
			wp_trash_post( $hello->ID );
			$log[] = array( 'ok', 'Moved WordPress’s sample “Hello world!” post to the Trash.' );
		}
	}
	if ( $opt['pages'] ) { $log = array_merge( $log, bmpc_import_pages( $data['pages'], $opt['overwrite'], $opt['seo'] ) ); }
	if ( $opt['reading'] ) {
		$home = get_page_by_path( 'home' ); $news = get_page_by_path( 'news' );
		if ( $home ) { update_option( 'show_on_front', 'page' ); update_option( 'page_on_front', $home->ID ); }
		if ( $news ) { update_option( 'page_for_posts', $news->ID ); }
		$log[] = $home ? array( 'ok', 'Front page set to হোম, posts page set to সর্বশেষ সংবাদ.' ) : array( 'warn', 'হোম page not found; front page not changed.' );
	}
	if ( $opt['menu'] ) { $log[] = bmpc_build_menu( $opt['overwrite'] ); }
	if ( ! get_option( 'permalink_structure' ) ) {
		$log[] = array( 'warn', 'Permalinks are “Plain”. Set Settings → Permalinks → “Post name” for clean URLs like /about/.' );
	}
	flush_rewrite_rules();
	return $log;
}

/** Copy theme images into the Media Library once. */
function bmpc_import_images( $images ) {
	require_once ABSPATH . 'wp-admin/includes/image.php';
	$map = get_option( 'bmpc_media', array() ); $log = array(); $n = 0;
	foreach ( $images as $img ) {
		$file = $img['file'];
		if ( ! empty( $map[ $file ] ) && get_post( $map[ $file ] ) ) { continue; }
		$src = BMPC_DIR . '/assets/img/' . $file;
		if ( ! file_exists( $src ) ) { continue; }
		$up = wp_upload_bits( 'bmpc-' . $file, null, file_get_contents( $src ) );
		if ( ! empty( $up['error'] ) ) { $log[] = array( 'warn', 'Image ' . esc_html( $file ) . ': ' . esc_html( $up['error'] ) ); continue; }
		$type = wp_check_filetype( $up['file'] );
		$id   = wp_insert_attachment( array( 'post_mime_type' => $type['type'], 'post_title' => $img['alt'] ? $img['alt'] : $file, 'post_status' => 'inherit' ), $up['file'] );
		if ( is_wp_error( $id ) || ! $id ) { continue; }
		wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $up['file'] ) );
		if ( $img['alt'] ) { update_post_meta( $id, '_wp_attachment_image_alt', $img['alt'] ); }
		$map[ $file ] = $id; $n++;
	}
	update_option( 'bmpc_media', $map );
	$log[] = array( 'ok', $n ? "$n images added to the Media Library." : 'Images already in the Media Library.' );
	if ( ! empty( $map['logo.png'] ) && ! has_site_icon() ) {
		update_option( 'site_icon', (int) $map['logo.png'] );
		$log[] = array( 'ok', 'Site icon set to the BMPC logo.' );
	}
	return $log;
}

/** Replace {{IMG:…}}, {{URL:…}}, {{POST:…}} and {{FLUENTFORM}} placeholders. */
function bmpc_resolve( $html ) {
	$html = preg_replace_callback( '/\{\{IMG:([^}]+)\}\}/', function ( $m ) { return esc_url( bmpc_media_url( $m[1] ) ); }, $html );
	$html = preg_replace_callback( '/\{\{URL:([^}]+)\}\}/', function ( $m ) { return esc_url( 'home' === $m[1] ? home_url( '/' ) : bmpc_page_url( $m[1] ) ); }, $html );
	$html = preg_replace_callback( '/\{\{POST:([^}]+)\}\}/', function ( $m ) {
		$p = get_posts( array( 'post_type' => 'post', 'meta_key' => 'bmpc_stem', 'meta_value' => $m[1], 'numberposts' => 1, 'post_status' => 'any' ) );
		return esc_url( $p ? get_permalink( $p[0] ) : bmpc_page_url( 'news' ) );
	}, $html );
	if ( false !== strpos( $html, '{{FLUENTFORM}}' ) ) {
		$html = str_replace( '{{FLUENTFORM}}', bmpc_fluentform_shortcode(), $html );
	}
	return $html;
}

function bmpc_fluentform_shortcode() {
	global $wpdb;
	$table = $wpdb->prefix . 'fluentform_forms';
	$found = $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $table ) );
	if ( $found ) {
		$id = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM {$table} WHERE title LIKE %s ORDER BY id DESC LIMIT 1", $wpdb->esc_like( 'সদস্য আবেদন ফর্ম' ) . '%' ) );
		if ( $id ) { return '[fluentform id="' . (int) $id . '"]'; }
	}
	return '<p class="note-draft">সদস্য আবেদন ফর্মটি এখনো যুক্ত হয়নি। Fluent Forms-এ ফর্ম ইমপোর্ট করে BMPC Setup আবার চালান।</p>';
}

function bmpc_seo_meta( $id, $title, $desc ) {
	update_post_meta( $id, 'rank_math_title', $title );
	update_post_meta( $id, 'rank_math_description', $desc );
	update_post_meta( $id, '_yoast_wpseo_title', $title );
	update_post_meta( $id, '_yoast_wpseo_metadesc', $desc );
}

function bmpc_import_pages( $pages, $overwrite, $seo ) {
	$log = array(); $ids = array();
	foreach ( $pages as $i => $p ) {
		$existing = get_page_by_path( $p['slug'] );
		if ( $existing && ! $overwrite ) {
			$log[] = array( 'skip', 'Page “' . esc_html( $p['title'] ) . '” (/' . esc_html( $p['slug'] ) . '/) already exists; skipped.' );
			continue;
		}
		$args = array( 'post_type' => 'page', 'post_status' => 'publish', 'post_title' => $p['title'], 'post_name' => $p['slug'],
			'post_content' => $p['content'], 'menu_order' => $i, 'comment_status' => 'closed' );
		if ( $existing ) { $args['ID'] = $existing->ID; }
		$id = wp_insert_post( wp_slash( $args ), true );
		if ( is_wp_error( $id ) ) { $log[] = array( 'warn', esc_html( $p['title'] ) . ': ' . esc_html( $id->get_error_message() ) ); continue; }
		update_post_meta( $id, '_et_pb_use_builder', 'news' === $p['slug'] ? 'off' : 'on' );
		update_post_meta( $id, '_et_pb_page_layout', 'et_full_width_page' );
		update_post_meta( $id, '_et_pb_side_nav', 'off' );
		update_post_meta( $id, '_et_pb_show_title', 'off' );
		update_post_meta( $id, '_et_builder_version', 'VB|Divi|4.27.4' );
		update_post_meta( $id, '_wp_page_template', 'default' );
		if ( $seo ) { bmpc_seo_meta( $id, $p['seo_title'], $p['seo_desc'] ); }
		$ids[ $id ] = $p['content'];
		$log[] = array( 'ok', ( $existing ? 'Updated' : 'Created' ) . ' page “' . esc_html( $p['title'] ) . '”.' );
	}
	// Second pass: links between pages resolve once every page exists.
	foreach ( $ids as $id => $content ) {
		wp_update_post( wp_slash( array( 'ID' => $id, 'post_content' => bmpc_resolve( $content ) ) ) );
	}
	return $log;
}

function bmpc_import_posts( $posts, $overwrite, $seo ) {
	$log = array(); $map = get_option( 'bmpc_media', array() );
	foreach ( $posts as $p ) {
		$found = get_posts( array( 'post_type' => 'post', 'meta_key' => 'bmpc_stem', 'meta_value' => $p['stem'], 'numberposts' => 1, 'post_status' => 'any' ) );
		if ( $found && ! $overwrite ) { $log[] = array( 'skip', 'News “' . esc_html( $p['title'] ) . '” already exists; skipped.' ); continue; }
		$cat = get_term_by( 'name', $p['category'], 'category' );
		if ( ! $cat ) { $t = wp_insert_term( $p['category'], 'category' ); $cat_id = is_wp_error( $t ) ? 0 : $t['term_id']; } else { $cat_id = $cat->term_id; }
		$args = array( 'post_type' => 'post', 'post_status' => 'publish', 'post_title' => $p['title'], 'post_name' => $p['stem'],
			'post_content' => bmpc_resolve( $p['content'] ), 'post_excerpt' => $p['summary'], 'post_date' => $p['date'],
			'post_category' => $cat_id ? array( $cat_id ) : array() );
		if ( $found ) { $args['ID'] = $found[0]->ID; }
		$id = wp_insert_post( wp_slash( $args ), true );
		if ( is_wp_error( $id ) ) { $log[] = array( 'warn', esc_html( $id->get_error_message() ) ); continue; }
		update_post_meta( $id, 'bmpc_stem', $p['stem'] );
		update_post_meta( $id, 'bmpc_event', $p['event'] );
		update_post_meta( $id, 'bmpc_place', $p['place'] );
		update_post_meta( $id, 'bmpc_summary', $p['summary'] );
		if ( ! empty( $map[ $p['image'] ] ) ) { set_post_thumbnail( $id, (int) $map[ $p['image'] ] ); }
		if ( $seo ) { bmpc_seo_meta( $id, $p['seo_title'], $p['seo_desc'] ); }
		$log[] = array( 'ok', ( $found ? 'Updated' : 'Created' ) . ' news “' . esc_html( $p['title'] ) . '”.' );
	}
	return $log;
}

function bmpc_build_menu( $overwrite ) {
	$name = 'BMPC প্রধান মেনু';
	$menu = wp_get_nav_menu_object( $name );
	if ( $menu && ! $overwrite ) {
		bmpc_assign_menu( $menu->term_id );
		return array( 'skip', 'Menu “' . $name . '” already exists; assigned to Primary Menu.' );
	}
	if ( $menu ) { wp_delete_nav_menu( $menu->term_id ); }
	$menu_id = wp_create_nav_menu( $name );
	if ( is_wp_error( $menu_id ) ) { return array( 'warn', esc_html( $menu_id->get_error_message() ) ); }
	$add = function ( $title, $args, $parent = 0 ) use ( $menu_id ) {
		return wp_update_nav_menu_item( $menu_id, 0, array_merge( array( 'menu-item-title' => $title, 'menu-item-status' => 'publish', 'menu-item-parent-id' => $parent ), $args ) );
	};
	$page = function ( $slug ) {
		$p = get_page_by_path( $slug );
		return $p ? array( 'menu-item-object' => 'page', 'menu-item-object-id' => $p->ID, 'menu-item-type' => 'post_type' ) : array( 'menu-item-url' => home_url( '/' . $slug . '/' ), 'menu-item-type' => 'custom' );
	};
	$add( 'হোম', array( 'menu-item-url' => home_url( '/' ), 'menu-item-type' => 'custom' ) );
	$about = $add( 'আমাদের সম্পর্কে', $page( 'about' ) );
	$add( 'পরিচিতি ও নীতিমালা', $page( 'about' ), $about );
	$add( 'ঘোষণাপত্র', $page( 'manifesto' ), $about );
	$add( 'গঠনতন্ত্র', $page( 'constitution' ), $about );
	$add( 'লক্ষ্য ও উদ্দেশ্য', $page( 'objectives' ), $about );
	$msg = $add( 'বাণী', array( 'menu-item-url' => '#', 'menu-item-type' => 'custom' ) );
	$add( 'চেয়ারম্যানের বাণী', $page( 'chairman-message' ), $msg );
	$add( 'মহাসচিবের বাণী', $page( 'secretary-general-message' ), $msg );
	$add( 'সর্বশেষ সংবাদ', $page( 'news' ) );
	$add( 'যোগাযোগ', array( 'menu-item-url' => '#footer', 'menu-item-type' => 'custom' ) );
	bmpc_assign_menu( $menu_id );
	return array( 'ok', 'Menu “' . $name . '” created and assigned to Primary Menu.' );
}

function bmpc_assign_menu( $menu_id ) {
	$loc = get_theme_mod( 'nav_menu_locations', array() );
	$loc['primary-menu'] = (int) $menu_id;
	set_theme_mod( 'nav_menu_locations', $loc );
}
