import unittest
import time
from instrument import AnomalyDetector  # Your AnomalyDetector class location

class TestAnomalyDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = AnomalyDetector()
        now = time.time()
        cls.now = now

        # Register users once for all tests
        cls.detector.instrument("register", "ADMIN", "123", "008777", now, {})
        cls.detector.instrument("register", "USER", "124", "004281", now, {})
        cls.detector.instrument("register", "MANAGER", "125", "002141", now, {})
        cls.detector.instrument("register", "USER", "126", "006426", now, {})



    # --- Rate anomaly tests ---

    def test_failed_login_user(self):
        print("Testing failed login rate for USER (flag after 6 failures in 60s)")
        base_time = time.time()
        flagged = False
        for i in range(6):  # USER limit is 5 failures per 60s
            flagged = self.detector.instrument(
                "login_attempt", "USER", "user1", "src1",
                base_time + i * 10,
                {"status": "failure"}
            )
        self.assertTrue(flagged)

    def test_failed_login_admin(self):
        print("Testing failed login rate for ADMIN (flag after 11 failures in 60s)")
        base_time = time.time()
        flagged = False
        for i in range(11):  # ADMIN limit is 10 failures per 60s (2x user limit)
            flagged = self.detector.instrument(
                "login_attempt", "ADMIN", "admin1", "src2",
                base_time + i * 5,
                {"status": "failure"}
            )
        self.assertTrue(flagged)

    def test_toggle_device_user(self):
        print("Testing toggle device spam for USER (flag after 11 toggles in 30s)")
        base_time = time.time()
        flagged = False
        for i in range(11):  # USER limit is 10 toggles per 30s
            flagged = self.detector.instrument(
                "toggle_device", "USER", "user2", "src3",
                base_time + i * 2,
                {"device_name": "fan"}
            )
        self.assertTrue(flagged)

    def test_toggle_device_admin(self):
        print("Testing toggle device spam for ADMIN (flag after 21 toggles in 30s)")
        base_time = time.time()
        flagged = False
        for i in range(21):  # ADMIN limit is 20 toggles per 30s (2x user limit)
            flagged = self.detector.instrument(
                "toggle_device", "ADMIN", "admin2", "src4",
                base_time + i,
                {"device_name": "light"}
            )
        self.assertTrue(flagged)

    def test_normal_toggle_use(self):
        base_time = time.time()
        user_id = 'user3'
        source_id = 'src5'
        self.detector.instrument('register', 'USER', user_id, source_id, base_time, {})

        flagged = False
        for i in range(10):  # Exactly at limit, should NOT flag
            flagged |= self.detector.instrument('toggle_device', 'USER', user_id, source_id, base_time + i * 3, {})
        self.assertFalse(flagged)

    def test_password_change_rate(self):
        base_time = time.time()
        user_id = "user_pw"
        flagged = False
        for i in range(3):  # More than 2 changes in 30 mins triggers flag
            flagged = self.detector.instrument("password_change", "USER", user_id, "src_pw", base_time + i * 600, {})
        self.assertTrue(flagged)

    def test_device_registration_rate(self):
        print("Testing device registration rate limit")
        base_time = time.time()
        
        # Register a test user first
        self.detector.instrument("register", "USER", "test_user", "test_src", base_time, {})
        
        # Verify registration worked
        self.assertIn("test_user", self.detector.regUsers)
        
        flagged = False
        for i in range(6):  # USER limit is 5 registrations per hour
            result = self.detector.instrument(
                "device_registration",
                "USER",
                "test_user",
                f"src_{i}",
                base_time + i * 600,  # 10 minutes apart
                {"device_id": f"dev_{i}"}
            )
            flagged = flagged or result  # Capture any True results
        
        self.assertTrue(flagged, "Should flag after exceeding device registration limit")



if __name__ == '__main__':
    unittest.main()
