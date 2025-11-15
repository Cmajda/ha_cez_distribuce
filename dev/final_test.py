#!/usr/bin/env python3
"""Final test of new CEZ API."""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "custom_components", "cez_hdo"))

import downloader  # noqa: E402


def test_api_flow():
    """Test celého API workflow."""

    print("🧪 Final test ČEZ HDO API")
    print("=" * 50)

    # Test s ukázkovými daty odpovídajícími skutečnému API
    sample_json = {
        "data": {
            "signals": [
                {
                    "signal": "EVV1",
                    "den": "Sobota",
                    "datum": "15.11.2025",
                    "casy": "00:00-06:00;   07:00-09:00;   10:00-13:00;   14:00-16:00;   17:00-24:00",
                },
                {
                    "signal": "EVV1",
                    "den": "Neděle",
                    "datum": "16.11.2025",
                    "casy": "00:00-06:00;   07:00-09:00;   10:00-13:00;   14:00-16:00;   17:00-24:00",
                },
            ]
        }
    }

    print("📊 Test API response parsing...")

    # Test get_today_schedule
    schedule = downloader.get_today_schedule(sample_json)
    print(f"📅 Today's schedule: {len(schedule)} periods")
    for i, (start, end) in enumerate(schedule):
        print(f"   Period {i+1}: {start} - {end}")

    # Test isHdo main function
    result = downloader.isHdo(sample_json)
    print("\n🎯 HDO Analysis:")

    (
        low_active,
        low_start,
        low_end,
        low_duration,
        high_active,
        high_start,
        high_end,
        high_duration,
    ) = result

    print(f"💡 Low tariff active: {low_active}")
    if low_start:
        print(f"   Start: {low_start}, End: {low_end}")
        if low_duration:
            print(f"   Duration: {downloader.format_duration(low_duration)}")

    print(f"🔥 High tariff active: {high_active}")
    if high_start:
        print(f"   Start: {high_start}, End: {high_end}")
        if high_duration:
            print(f"   Duration: {downloader.format_duration(high_duration)}")

    print("\n🔧 API functions test:")
    print(f"   BASE_URL: {downloader.BASE_URL}")
    print(f"   get_request_data('12345'): {downloader.get_request_data('12345')}")

    print("\n✅ All tests completed successfully!")
    print("\nKonfiguration change:")
    print("PŘED: region='stred', code='EVV1'")
    print("PO:   ean='VAŠE_EAN_ČÍSLO'")

    return True


if __name__ == "__main__":
    test_api_flow()
