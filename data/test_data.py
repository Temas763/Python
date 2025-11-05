from datetime import datetime, timedelta

class TestData:
    # Test event data
    @staticmethod
    def get_event_data():
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        return {
            "title": "Test Event",
            "description": "Test Description",
            "startAt": start_time.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "endAt": end_time.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "backgroundColor": "#F4F5F6",
            "color": "#81888D"
        }
    
    @staticmethod
    def get_schedule_period():
        from_date = datetime.now()
        till_date = from_date + timedelta(days=7)
        
        return {
            "from": from_date.strftime("%Y-%m-%dT00:00:00+03:00"),
            "till": till_date.strftime("%Y-%m-%dT00:00:00+03:00")
        }
    
    # Invalid data for negative tests
    INVALID_EVENT_DATA = {
        "title": "A" * 1000,  # Very long title
        "startAt": "invalid_date",
        "endAt": "invalid_date"
    }
    
    EVENT_WITH_START_AFTER_END = {
        "title": "Invalid Time Event",
        "startAt": "2025-05-27T20:30:00+03:00",
        "endAt": "2025-05-27T20:00:00+03:00",
        "backgroundColor": "#F4F5F6",
        "color": "#81888D"
    }