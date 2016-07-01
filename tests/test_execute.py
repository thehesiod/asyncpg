import asyncpg
from asyncpg import _testbase as tb


class TestExecuteScript(tb.ConnectedTestCase):

    async def test_execute_script_1(self):
        r = await self.con.execute('''
            SELECT 1;

            SELECT true FROM pg_type WHERE false = true;

            SELECT 2;
        ''')
        self.assertIsNone(r)

    async def test_execute_script_check_transactionality(self):
        with self.assertRaises(asyncpg.Error):
            await self.con.execute('''
                CREATE TABLE mytab (a int);
                SELECT * FROM mytab WHERE 1 / 0 = 1;
            ''')

        with self.assertRaisesRegex(asyncpg.Error, '"mytab" does not exist'):
            await self.con.prepare('''
                SELECT * FROM mytab
            ''')
