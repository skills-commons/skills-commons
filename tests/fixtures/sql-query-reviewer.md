SELECT u.id, u.email, COUNT(o.id) AS orders
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
LEFT JOIN refunds r ON r.order_id = o.id
WHERE u.created_at > '2026-01-01' AND r.id IS NULL
GROUP BY u.id
ORDER BY orders DESC;

PostgreSQL. users has 4M rows, orders 40M.
