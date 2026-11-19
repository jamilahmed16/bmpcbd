<?php
/** Single news post. */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
while ( have_posts() ) : the_post();
	$event = get_post_meta( get_the_ID(), 'bmpc_event', true );
	$place = get_post_meta( get_the_ID(), 'bmpc_place', true );
	$news  = get_option( 'page_for_posts' ) ? get_permalink( get_option( 'page_for_posts' ) ) : bmpc_page_url( 'news' );
	?>
<main id="main-content">
<section class="hero phero"><div class="wrap"><div style="display:grid;gap:14px">
	<nav class="crumbs" aria-label="অবস্থান"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">হোম</a><span aria-hidden="true">/</span><a href="<?php echo esc_url( $news ); ?>">সর্বশেষ সংবাদ</a><span aria-hidden="true">/</span><span>সংবাদ</span></nav>
	<h1><?php the_title(); ?></h1>
</div></div></section>
<article class="post"><div class="wrap">
	<div class="meta"><?php $cat = get_the_category(); if ( $cat ) : ?><span class="chip-cat"><?php echo esc_html( $cat[0]->name ); ?></span><?php endif; ?><time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( bmpc_bn_date() ); ?></time><span><?php the_author(); ?></span></div>
	<?php if ( has_post_thumbnail() ) : ?>
	<figure><?php the_post_thumbnail( 'large' ); ?><?php $cap = get_the_post_thumbnail_caption(); if ( $cap || $place ) : ?><figcaption><?php echo esc_html( $cap ? $cap : $place ); ?></figcaption><?php endif; ?></figure>
	<?php endif; ?>
	<?php if ( $event ) : $parts = array_map( 'trim', explode( '·', $event ) ); $labels = array( 'কর্মসূচি', 'তারিখ', 'সময়', 'স্থান' ); ?>
	<div class="event" aria-label="কর্মসূচির তথ্য"><?php foreach ( $parts as $k => $p ) : ?><div><small><?php echo esc_html( $labels[ $k ] ?? '' ); ?></small><b><?php echo esc_html( $p ); ?></b></div><?php endforeach; ?></div>
	<?php endif; ?>
	<div class="body"><?php the_content(); ?></div>
	<a class="back" href="<?php echo esc_url( $news ); ?>">← সব সংবাদ</a>
</div></article>
</main>
<?php endwhile;
get_footer();
