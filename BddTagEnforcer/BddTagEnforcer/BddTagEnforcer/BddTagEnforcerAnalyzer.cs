using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Diagnostics;
using System.Collections.Immutable;
using System.Linq;

[DiagnosticAnalyzer(LanguageNames.CSharp)]
public class BddTagEnforcerAnalyzer : DiagnosticAnalyzer
{
    public const string DiagnosticId = "BddTagEnforcer";

    private static DiagnosticDescriptor Rule = new DiagnosticDescriptor(
        DiagnosticId,
        "String variable 'BddFeatureMapper' is missing",
        "The required variable 'BddFeatureMapper' is missing.",
        "Naming",
        DiagnosticSeverity.Error,
        isEnabledByDefault: true,
        description: "Ensure that the required variable 'BddFeatureMapper' is always present.");

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics => ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        context.RegisterSyntaxNodeAction(AnalyzeClassDeclaration, SyntaxKind.ClassDeclaration);
    }

    private static void AnalyzeClassDeclaration(SyntaxNodeAnalysisContext context)
    {
        var classDeclaration = (ClassDeclarationSyntax)context.Node;

        if (ShouldSkipAnalysis(classDeclaration))
        {
            return;
        }

        if (!ContainsRequiredVariable(classDeclaration, "BddFeatureMapper"))
        {
            var diagnostic = Diagnostic.Create(Rule, classDeclaration.Identifier.GetLocation());
            context.ReportDiagnostic(diagnostic);
        }
    }

    private static bool ShouldSkipAnalysis(ClassDeclarationSyntax classDeclaration)
    {
        if (classDeclaration.Modifiers.Any(SyntaxKind.InterfaceKeyword) ||
            classDeclaration.Modifiers.Any(SyntaxKind.AbstractKeyword) ||
            classDeclaration.Modifiers.Any(SyntaxKind.EnumKeyword))
        {
            return true;
        }

        return ContainsOnlyPropertiesOrStrings(classDeclaration);
    }

    private static bool ContainsRequiredVariable(ClassDeclarationSyntax classDeclaration, string variableName)
    {
        foreach (var member in classDeclaration.Members)
        {
            if (member is FieldDeclarationSyntax fieldDeclaration)
            {
                foreach (var variable in fieldDeclaration.Declaration.Variables)
                {
                    if (variable.Identifier.Text == variableName)
                    {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    private static bool ContainsOnlyPropertiesOrStrings(ClassDeclarationSyntax classDeclaration)
    {
        foreach (var member in classDeclaration.Members)
        {
            if (member is PropertyDeclarationSyntax propertyDeclaration)
            {
                if (!propertyDeclaration.Modifiers.Any(SyntaxKind.SetKeyword))
                {
                    continue;
                }
            }
            else if (member is FieldDeclarationSyntax fieldDeclaration)
            {
                if (fieldDeclaration.Declaration.Type.ToString() != "string")
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
        }
        return true;
    }
}
