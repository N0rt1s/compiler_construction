public class Tokenization
{

    public Tokenization() { }
    public char[] splittables = { ' ', ';' };
    public char[] operators = { '+', '-', '=', '/', '*', '(', ')', '{', '}', '%','"' };
    public string[] keyWords = { "public", "private", "static", "class", "function", "struct", "new", "return", "break", "continue", "if", "else", "while", "for", "forEach", "switch", "case"};
    public string[] dataTypes = { "number", "string", "char", "bool", "void" };
    public string[] arrayDataTypes = { "number[]", "string[]", "char[]" };

    public List<string> MakeTokens(string line)
    {
        List<string> tokens = new List<string>();
        if (line[line.Length - 1] != ';')
        {
            // tokens.Add("Error");
            return null;
        }
        string token = string.Empty;
        foreach (var item in line)
        {
            // Console.WriteLine($"item is {item} and is {splittables.Contains(item)}");
            if (splittables.Contains(item))
            {
                // Console.WriteLine(token);
                tokens.Add(token);
                token = string.Empty;
            }
            else if (operators.Contains(item))
            {
                tokens.Add(token);
                tokens.Add(item.ToString());
                token = string.Empty;
            }
            token += item;

        }
        Console.WriteLine(tokens.Count);
        return tokens;
    }


}