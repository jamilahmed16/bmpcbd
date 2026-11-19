<?php
/** News list (the page set as "Posts page" in Settings → Reading). */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
$paged = max( 1, (int) get_query_var( 'paged' ) );
?>
<main id="main-content">
<section class="hero phero"><div class="wrap"><div style="display:grid;gap:14px">
	<nav class="crumbs" aria-label="অবস্থান"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">হোম</a><span aria-hidden="true">/</span><span>সর্বশেষ সংবাদ</span></nav>
	<h1>সর্বশেষ সংবাদ</h1>
	<p class="lede">কাউন্সিলের কর্মসূচি, মানববন্ধন, দিবস পালন ও সাংগঠনিক কার্যক্রমের খবর।</p>
</div></div></section>
<?php if ( have_posts() ) : $i = 0; ?>
	<?php while ( have_posts() ) : the_post(); $i++; $big = ( 1 === $i && 1 === $paged ); ?>
		<?php if ( $big ) : ?><section class="feat"><div class="wrap"><?php elseif ( 2 === $i || ( 1 === $i && $paged > 1 ) ) : ?><section class="grid-sec"><div class="wrap"><h2 class="sr">আরও সংবাদ</h2><div class="ngrid"><?php endif; ?>
		<a class="story<?php echo $big ? ' big' : ''; ?>" href="<?php the_permalink(); ?>">
			<?php if ( has_post_thumbnail() ) { the_post_thumbnail( $big ? 'large' : 'medium_large', array( 'loading' => $big ? 'eager' : 'lazy' ) ); } ?>
			<div class="txt"><div class="meta"><?php $cat = get_the_category(); if ( $cat ) : ?><span class="chip-cat"><?php echo esc_html( $cat[0]->name ); ?></span><?php endif; ?><time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( bmpc_bn_date() ); ?></time></div>
			<h2><?php the_title(); ?></h2><?php if ( $big ) : ?><p><?php echo esc_html( wp_trim_words( get_the_excerpt(), 40, '…' ) ); ?></p><?php endif; ?><span class="more">পুরো সংবাদ পড়ুন →</span></div>
		</a>
		<?php if ( $big ) : ?></div></section><?php endif; ?>
	<?php endwhile; ?>
	<?php if ( $i > 1 || $paged > 1 ) : ?></div></div></section><?php endif; ?>
	<div class="wrap bmpc-pager"><?php the_posts_pagination( array( 'prev_text' => '← আগের', 'next_text' => 'পরের →' ) ); ?></div>
	<?php if ( 1 === $i && 1 === $paged ) : ?>
	<section class="empty"><div class="wrap"><div class="box"><div><b>আরও সংবাদ শীঘ্রই</b><p>নতুন পোস্ট প্রকাশ হলে এখানে তালিকা আকারে দেখা যাবে।</p></div><a class="btn btn-green" href="<?php echo esc_url( bmpc_page_url( 'join' ) ); ?>">সদস্য হোন</a></div></div></section>
	<?php endif; ?>
<?php else : ?>
	<section class="empty" style="padding-top:64px"><div class="wrap"><div class="box"><div><b>এখনো কোনো সংবাদ নেই</b><p>প্রথম সংবাদ প্রকাশ হলে এখানে দেখা যাবে।</p></div></div></div></section>
<?php endif; ?>
</main>
<?php get_footer();
