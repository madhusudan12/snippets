from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.pool import NullPool

EXCLUDE_CATEGORIES = (
    "test", "mezzaninetest", "promo", "top_articles",
    "Sierra Leone promo", "India promo", "Test in India",
    "Test in US", "Testing India Football"
)


def check_db():
    kwargs = {}
    kwargs["poolclass"] = NullPool
    db = scoped_session(sessionmaker(bind=create_engine(
    'postgresql://duta:dutapassword@%(duta_pg_curation_host_port)s/curation', **kwargs),autocommit=True))
    lookback_interval=86400
    where_clause = "AND updated >= now() - ':lookback seconds'::interval"
    query = """
    SELECT bb.id as id, bb.created, bb.updated, bb.content, bb.title, bb.slug, bb.description, ba.language,
        array_agg(bp.category) categories, min(bp.ctime) as published
    FROM blog_blogpost bb
        JOIN blogger_articles ba ON (bb.id = ba.blogpost_ptr_id)
        JOIN blogger_published bp on (ba.article_hash = bp.article_hash)
    WHERE bp.category NOT IN :exclude
        AND ba.source NOT IN ('duta_listing', 'duta_digest', 'duta_slide_show', 'duta_poll')
        {where_clause}
    GROUP BY 1,2,3,4,5,6,7,8""".format(where_clause=where_clause)

    db.execute(query, {'lookback': lookback_interval,
                       'exclude': EXCLUDE_CATEGORIES})





'''
SELECT bb.id as id, bb.created, bb.updated, bb.content, bb.title, bb.slug, bb.description, ba.language,
    array_agg(bp.category) categories, min(bp.ctime) as published
FROM blog_blogpost bb
    JOIN blogger_articles ba ON (bb.id = ba.blogpost_ptr_id)
    JOIN blogger_published bp on (ba.article_hash = bp.article_hash)
WHERE bp.category NOT IN ('test','promo','top_articles','India promo')
    AND ba.source NOT IN ('duta_listing', 'duta_digest', 'duta_slide_show', 'duta_poll')
    AND updated >= now() - '86400'::interval
    AND extract(month from bb.publish_date) = '12' 
    AND extract(year from bb.publish_date) = '2018'
GROUP BY 1,2,3,4,5,6,7,8;

'''

if __name__ == '__main__':
    check_db()


