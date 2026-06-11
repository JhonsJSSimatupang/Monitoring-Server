#!/bin/bash
# load-test.sh — Generate traffic ke Flask app untuk demo monitoring

BASE_URL="http://localhost:5000"
DURATION=${1:-60}  # default 60 detik
echo "🚀 Memulai load test selama ${DURATION} detik..."
echo "   Target: $BASE_URL"
echo "   Tekan Ctrl+C untuk berhenti"
echo ""

END=$((SECONDS + DURATION))

while [ $SECONDS -lt $END ]; do
    # Hit berbagai endpoint secara acak
    ENDPOINTS=("/" "/api/data" "/api/slow" "/api/error" "/health")
    EP=${ENDPOINTS[$RANDOM % ${#ENDPOINTS[@]}]}

    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$EP")
    echo "  [$(date +%H:%M:%S)] GET $EP → HTTP $STATUS"

    # Jeda acak 0.1–0.5 detik
    sleep $(awk "BEGIN{printf \"%.1f\", $RANDOM/32767 * 0.4 + 0.1}")
done

echo ""
echo "✅ Load test selesai!"
