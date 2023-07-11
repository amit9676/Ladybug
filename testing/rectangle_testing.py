import unittest

''' rectangle testing class - this unittesting class purpose is to the test the rectangles calculations function
in which we select a random point to place our war-wagon in it. in order to do that we a. take the intersection of
the 2 input rectangles - this is the in the method "get_intersection_rect".
b. we remove the intersection from one of the rectangle, and return the rectangle, or rectangles without the
intersection part. this is to avoid to count the intersection twice - increasing the chance of it being selected.
c. we take a random rectangle, and in it a random point - on it we will place the war wagon for operation.
this class will test the functionality of all these with arbitrary example - covering end cases.
all the rectangle functions work with the following input:
((top-left), (top-right), (bottom-right), (bottom-left)) that each of them is (x,y) tuple and represents a rectnagle
corner. the function will work ONLY on rectangles which sides are parallel to x,y axis.'''
class TestGetIntersectionRect(unittest.TestCase):
    def get_intersection_rect(self, rect_a, rect_b):
        # Compute the bounding box of the intersection of the two rectangles
        left = max(rect_a[0][0], rect_b[0][0])
        right = min(rect_a[1][0], rect_b[1][0])
        top = max(rect_a[0][1], rect_b[0][1])
        bottom = min(rect_a[2][1], rect_b[2][1])

        # Check if there is an intersection
        if left < right and top < bottom:
            # Return the intersection rectangle
            return ((left, top), (right, top), (right, bottom), (left, bottom))
        else:
            # Return None if there is no intersection
            return None


    def remove_intersection_rect(self, rect, intersection):
        # Calculate the four sides of the intersection rectangle


        return result_rectangles



    def test_intersection_exists(self):
        rect_a = ((0, 0), (10, 0), (10, 10), (0, 10))
        rect_b = ((5, 5), (15, 5), (15, 15), (5, 15))
        expected_intersection = ((5, 5), (10, 5), (10, 10), (5, 10))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_intersection_does_not_exist(self):
        rect_a = ((0, 0), (10, 0), (10, 10), (0, 10))
        rect_b = ((20, 20), (30, 20), (30, 30), (20, 30))
        expected_intersection = None
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_rectangles_overlap(self):
        rect_a = ((0, 0), (10, 0), (10, 10), (0, 10))
        rect_b = ((5, 5), (15, 5), (15, 15), (5, 15))
        expected_intersection = ((5, 5), (10, 5), (10, 10), (5, 10))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)


    def test_rectangles_identical(self):
        rect_a = ((0, 0), (10, 0), (10, 10), (0, 10))
        rect_b = ((0, 0), (10, 0), (10, 10), (0, 10))
        expected_intersection = ((0, 0), (10, 0), (10, 10), (0, 10))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_north_west(self):
        rect_a = ((50, 50), (150, 50), (150, 100), (50, 100))
        rect_b = ((50, 50), (100, 50), (100, 150), (50, 150))
        expected_intersection = ((50, 50), (100, 50), (100, 100), (50, 100))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_north_east(self):
        rect_a = ((50, 50), (150, 50), (150, 100), (50, 100))
        rect_b = ((100, 50), (150, 50), (150, 150), (100, 150))
        expected_intersection = ((100, 50), (150, 50), (150, 100), (100, 100))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_south_east(self):
        rect_a = ((50, 100), (150, 100), (150, 150), (50, 150))
        rect_b = ((100, 50), (150, 50), (150, 150), (100, 150))
        expected_intersection = ((100, 100), (150, 100), (150, 150), (100, 150))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_south_west(self):
        rect_a = ((50, 100), (150, 100), (150, 150), (50, 150))
        rect_b = ((50, 50), (100, 50), (100, 150), (50, 150))
        expected_intersection = ((50, 100), (100, 100), (100, 150), (50, 150))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_middle_intersect(self):
        rect_a = ((50, 80), (150, 80), (150, 130), (50, 130))
        rect_b = ((80, 50), (130, 50), (130, 150), (80, 150))
        expected_intersection = ((80, 80), (130, 80), (130, 130), (80, 130))
        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        self.assertEqual(actual_intersection, expected_intersection)

    def test_intersection_and_removal(self):
        rect_a = ((0, 0), (10, 0), (10, 10), (0, 10))
        rect_b = ((5, 5), (15, 5), (15, 15), (5, 15))
        expected_intersection = ((5, 5), (10, 5), (10, 10), (5, 10))
        expected_rectangles = [((0, 0), (5, 0), (5, 5), (0, 5)),
                               ((0, 5), (5, 5), (5, 10), (0, 10)),
                               ((5, 0), (10, 0), (10, 5), (0, 55)),
                               ((5, 5), (15, 5), (15, 15), (5, 15))]

        actual_intersection = self.get_intersection_rect(rect_a, rect_b)
        # Test get_intersection_rect
        self.assertEqual(actual_intersection, expected_intersection)

        # Test remove_intersection_rect
        result_rectangles = self.remove_intersection_rect(rect_a, self.get_intersection_rect(rect_a, actual_intersection))
        self.assertEqual(len(result_rectangles), len(expected_rectangles))
        for expected_rect in expected_rectangles:
            self.assertIn(expected_rect, result_rectangles)



if __name__ == '__main__':
    unittest.main()
