from datetime import datetime
import unittest
from unittest.mock import patch
import pandas as pd
from projectFunctions import read_csv, clean_data, add_borrow_duration_and_alert, drop_na, drop_duplicates, correct_dates, save_to_csv, fix_swapped_dates, fix_swapped_and_future_dates

class TestProjectFunctions(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_read_csv(self, mock_read_csv):
        # Arrange
        mock_df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        mock_read_csv.return_value = mock_df
        # Act
        result = read_csv('dummy.csv')
        # Assert
        mock_read_csv.assert_called_once_with('dummy.csv')
        pd.testing.assert_frame_equal(result, mock_df)

    def test_drop_na(self):
        # Arrange
        df = pd.DataFrame({'a': [1, None], 'b': [None, None]})
        # Act
        result = drop_na(df)
        result.loc[:, 'a'] = result['a'].astype('int')  # Explicitly cast column 'a' to int
        result.loc[:, 'b'] = result['b'].astype('int')  # Explicitly cast column 'b' to int
        # Assert
        expected = pd.DataFrame({'a': [1], 'b': [None]})
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_drop_duplicates(self):
        # Arrange
        df = pd.DataFrame({'a': [1, 1, 2], 'b': [3, 3, 4]})
        # Act
        result = drop_duplicates(df)
        # Assert
        expected = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_correct_dates(self):
        # Arrange
        df = pd.DataFrame({'date': ['01/01/2023', '32/01/2023', 'bad', '"02/02/2023"']})
        # Act
        result = correct_dates(df, 'date', default_date='01/01/2023')
        # Assert
        expected = pd.DataFrame({'date': [
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-02-02')
        ]})
        pd.testing.assert_frame_equal(result, expected)

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        df = pd.DataFrame({'a': [1, 2]})
        save_to_csv(df, 'output.csv')
        mock_to_csv.assert_called_once_with('output.csv', index=False)

    def test_fix_swapped_dates(self):
        df = pd.DataFrame({
            'Book checkout': ['2023-01-10', '2023-01-05'],
            'Book Returned': ['2023-01-05', '2023-01-10']
        })
        result = fix_swapped_dates(df.copy())
        # After fixing, all checkout dates should be <= returned dates
        self.assertTrue((pd.to_datetime(result['Book checkout']) <= pd.to_datetime(result['Book Returned'])).all())
        # The swap should have occurred for the first row
        self.assertEqual(result.loc[0, 'Book checkout'], pd.Timestamp('2023-01-05'))
        self.assertEqual(result.loc[0, 'Book Returned'], pd.Timestamp('2023-01-10'))

    def test_fix_swapped_and_future_dates(self):
        df = pd.DataFrame({
            'Book checkout': ['2023-01-10', '2023-01-05', '2023-01-01'],
            'Book Returned': ['2023-01-05', '2028-01-10', '2023-01-15']
        })
        result = fix_swapped_and_future_dates(df.copy(), max_year_diff=10)

        # Assert swapped dates are corrected
        self.assertEqual(result.loc[0, 'Book checkout'], pd.to_datetime('2023-01-05'))
        self.assertEqual(result.loc[0, 'Book Returned'], pd.to_datetime('2023-01-10'))

        # Assert future dates are corrected
        self.assertEqual(result.loc[1, 'Book checkout'], pd.to_datetime('2023-01-05'))
        self.assertEqual(result.loc[1, 'Book Returned'], pd.to_datetime('2023-01-10'))

        # Assert valid dates remain unchanged
        self.assertEqual(result.loc[2, 'Book checkout'], pd.to_datetime('2023-01-01'))
        self.assertEqual(result.loc[2, 'Book Returned'], pd.to_datetime('2023-01-15'))

    def test_add_borrow_duration_and_alert(self):
        df = pd.DataFrame({
            'Book checkout': ['2023-01-01', '2023-01-10', '2023-01-15', '2023-01-20'],
            'Book Returned': ['2023-01-10', '2023-01-25', None, '2023-01-30']
        })
        result = add_borrow_duration_and_alert(df.copy(), max_allowed_days=14)

        # Assert BorrowDuration column
        self.assertEqual(result.loc[0, 'BorrowDuration'], 9)  # Returned within 14 days
        self.assertEqual(result.loc[1, 'BorrowDuration'], 15)  # Returned after 14 days
        self.assertEqual(result.loc[2, 'BorrowDuration'], (pd.to_datetime(datetime.now().date()) - pd.to_datetime('2023-01-15')).days)  # Not returned yet
        self.assertEqual(result.loc[3, 'BorrowDuration'], 10)  # Returned within 14 days

        # Assert OverdueAlert column
        self.assertEqual(result.loc[0, 'OverdueAlert'], 'ON TIME')  # Returned within 14 days
        self.assertEqual(result.loc[1, 'OverdueAlert'], 'OVERDUE')  # Returned after 14 days
        self.assertEqual(result.loc[2, 'OverdueAlert'], 'SCHEDULED')  # Not returned yet
        self.assertEqual(result.loc[3, 'OverdueAlert'], 'ON TIME')  # Returned within 14 days

    @patch('projectFunctions.read_csv')
    @patch('projectFunctions.save_to_csv')
    def test_clean_data(self, mock_save_to_csv, mock_read_csv):
        # Arrange
        mock_df = pd.DataFrame({
            'Books': ['Book A', 'Book B', None],
            'Customer ID': [123, None, None],
            'Book checkout': ['2023-01-01', '2023-01-10', '2023-01-15'],
            'Book Returned': ['2023-01-10', '2028-01-25', None]
        })
        mock_read_csv.return_value = mock_df

        # Act
        result = clean_data(
            file_path='dummy.csv',
            date_columns=['Book checkout', 'Book Returned'],
            output_file='output.csv'
        )

        # Assert
        # Verify read_csv was called
        mock_read_csv.assert_called_once_with('dummy.csv')

        # Verify save_to_csv was called
        mock_save_to_csv.assert_called_once_with(result, 'output.csv')

        # Verify cleaned data
        expected_df = pd.DataFrame({
            'Books': ['Book A', 'Book B'],
            'Customer ID': [123, None],
            'Book checkout': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-10')],
            'Book Returned': [pd.Timestamp('2023-01-10'), pd.Timestamp('2023-01-25')],
            'BorrowDuration': [9, 15],
            'OverdueAlert': ['ON TIME', 'OVERDUE']
        })
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))


if __name__ == '__main__':
    unittest.main()