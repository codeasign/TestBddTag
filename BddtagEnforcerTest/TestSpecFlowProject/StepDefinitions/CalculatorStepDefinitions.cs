namespace TestSpecFlowProject.StepDefinitions
{
    [Binding]
    public sealed class CalculatorStepDefinitions
    {
        // For additional details on SpecFlow step definitions see https://go.specflow.org/doc-stepdef
        [Given(@"Run some Steps")]
        public void GivenRunSomeSteps()
        {
            Console.WriteLine("Steps were run");
        }

    }
}