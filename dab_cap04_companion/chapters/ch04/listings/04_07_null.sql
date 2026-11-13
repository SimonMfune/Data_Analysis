SELECT COUNT(*)            AS all_orders,
       COUNT(campaign_id)  AS with_campaign,
       COUNT(*) - COUNT(campaign_id) AS without_campaign
FROM orders;

SELECT COUNT(*) AS undelivered
FROM deliveries
WHERE delivered_at IS NULL;
