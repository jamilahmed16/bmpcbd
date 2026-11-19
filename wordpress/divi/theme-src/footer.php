<?php
/** BMPC footer (replaces Divi's footer). */
if ( ! defined( 'ABSPATH' ) ) { exit; }
$logo   = bmpc_media_url( 'logo.png' );
$social = bmpc_social();
$icons  = array(
	'facebook'  => array( 'Facebook', '<path fill="currentColor" d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.2V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.6-.6z"/>' ),
	'x'         => array( 'X', '<path fill="currentColor" d="M17.7 3h3.1l-6.8 7.8L22 21h-6.3l-4.9-6.4L5.2 21H2.1l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7.5 4.7H5.7z"/>' ),
	'instagram' => array( 'Instagram', '<path fill="currentColor" d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.9-8.9a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2zM12 2.5c-2.6 0-2.9 0-3.9.1C4.6 2.7 2.7 4.6 2.6 8.1c-.1 1-.1 1.3-.1 3.9s0 2.9.1 3.9c.1 3.5 2 5.4 5.5 5.5 1 .1 1.3.1 3.9.1s2.9 0 3.9-.1c3.5-.1 5.4-2 5.5-5.5.1-1 .1-1.3.1-3.9s0-2.9-.1-3.9c-.1-3.5-2-5.4-5.5-5.5-1-.1-1.3-.1-3.9-.1zm0 1.7c2.5 0 2.8 0 3.8.1 2.5.1 3.7 1.3 3.8 3.8.1 1 .1 1.3.1 3.8s0 2.8-.1 3.8c-.1 2.5-1.3 3.7-3.8 3.8-1 .1-1.3.1-3.8.1s-2.8 0-3.8-.1c-2.5-.1-3.7-1.3-3.8-3.8-.1-1-.1-1.3-.1-3.8s0-2.8.1-3.8C4.5 5.6 5.7 4.4 8.2 4.3c1-.1 1.3-.1 3.8-.1z"/>' ),
);
$cols = array(
	'সংগঠন'  => array( 'about' => 'আমাদের সম্পর্কে', 'manifesto' => 'ঘোষণাপত্র', 'constitution' => 'গঠনতন্ত্র', 'objectives' => 'লক্ষ্য ও উদ্দেশ্য' ),
	'অংশ নিন' => array( 'join' => 'সদস্য হোন', 'chairman-message' => 'চেয়ারম্যানের বাণী', 'secretary-general-message' => 'মহাসচিবের বাণী', 'news' => 'সর্বশেষ সংবাদ' ),
);
?>
<footer id="footer"><div class="wrap"><div class="cols">
	<div><a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>"><img class="logo" src="<?php echo esc_url( $logo ); ?>" width="68" height="68" alt=""><span><b>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</b></span></a>
	<p class="about-f">মুক্তিযুদ্ধের চেতনা ধারণকারী অরাজনৈতিক সংগঠন। বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের ঐক্যবদ্ধ প্ল্যাটফর্ম।</p>
	<div class="social" aria-label="সামাজিক যোগাযোগ">
		<?php foreach ( $icons as $key => $icon ) : if ( empty( $social[ $key ] ) ) { continue; } ?>
			<a href="<?php echo esc_url( $social[ $key ] ); ?>" aria-label="<?php echo esc_attr( $icon[0] ); ?>" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><?php echo $icon[1]; // phpcs:ignore -- static SVG ?></svg></a>
		<?php endforeach; ?>
		<a href="<?php echo esc_url( get_bloginfo( 'rss2_url' ) ); ?>" aria-label="সংবাদ (RSS)"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M5 17a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM3 10v3a8 8 0 0 1 8 8h3A11 11 0 0 0 3 10zm0-6v3a14 14 0 0 1 14 14h3A17 17 0 0 0 3 4z"/></svg></a>
	</div></div>
	<?php foreach ( $cols as $head => $links ) : ?>
	<div><h4><?php echo esc_html( $head ); ?></h4><ul>
		<?php foreach ( $links as $slug => $label ) : ?><li><a href="<?php echo esc_url( bmpc_page_url( $slug ) ); ?>"><?php echo esc_html( $label ); ?></a></li><?php endforeach; ?>
	</ul></div>
	<?php endforeach; ?>
</div><div class="legal"><span>© <?php echo esc_html( bmpc_bn_num( wp_date( 'Y' ) ) ); ?> বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</span><span>Developed by Rank On Fire LLC</span></div></div></footer>
</div><!-- #et-main-area -->
</div><!-- #page-container -->
<?php wp_footer(); ?>
</body>
</html>
