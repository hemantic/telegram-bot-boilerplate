from unittest.mock import patch

from src.tasks import track_amplitude


@patch('src.amplitude_helper.AmplitudeLogger.log')
def test_track_amplitude(mocked_log, bot_user, set_amplitude):
    track_amplitude(bot_user.chat_id, 'sample_event', event_properties={'prop1': 'val1'}, timestamp=12345)

    assert 56473829 == mocked_log.call_args.kwargs['user_id']
    assert 'sample_event' in mocked_log.call_args.kwargs['event']
    assert {'prop1': 'val1'} == mocked_log.call_args.kwargs['event_properties']
    assert 12345 == mocked_log.call_args.kwargs['timestamp']
