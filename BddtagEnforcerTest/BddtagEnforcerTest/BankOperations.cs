using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BddtagEnforcerTest
{
    abstract class BankOperations : IAccounts
    {
        public void OpenAccount()
        {
            throw new NotImplementedException();
        }

        public void CloseAccount()
        {
            throw new NotImplementedException();
        }
    }
}
