using System;
using System.Text.RegularExpressions;
public class Tokenization
{

    public Tokenization() { }
    public char[] operators = { '+', '-', '=', '/', '*', '%' };
    public char[] punctuators = { '(', ')', '{', '}', ';' };
    public string[] keyWords = { "public", "private", "static", "class", "function", "struct", "new", "return", "break", "continue", "if", "else", "while", "for", "forEach", "switch", "case" };
    public string[] dataTypes = { "number", "string", "char", "bool", "void" };
    public string[] arrayDataTypes = { "number[]", "string[]", "char[]" };
    string identifier = @"^[a-zA-Z_][a-zA-Z0-9_]*$";

    public List<Dictionary<string, string>> makeParts(List<string> list)
    {
        Console.WriteLine("Entered");
        var parts = new List<Dictionary<string, string>>();
        foreach (var item in list)
        {
            Dictionary<string, string> dictionary1 = new Dictionary<string, string>();

            if (operators.Contains(item[0]))
            {
                dictionary1["class"] = "Operator";
            }
            else if (punctuators.Contains(item[0]))
            {
                dictionary1["class"] = "Punctuators";
            }
            else if (keyWords.Contains(item))
            {
                dictionary1["class"] = "KeyWord";
            }
            else if (dataTypes.Contains(item))
            {
                dictionary1["class"] = "DataType";
            }
            else if (arrayDataTypes.Contains(item))
            {
                dictionary1["class"] = "ArrayDataType";
            }
            else if (Regex.IsMatch(item, "[\"]") || Regex.IsMatch(item, "[']"))
            {
                dictionary1["class"] = "Quotes";
            }
            else if (Regex.IsMatch(item, identifier))
            {
                dictionary1["class"] = "Identifier";
            }
            else
            {
                dictionary1["class"] = "InvalidToken";
            }

            dictionary1["value"] = item;
            parts.Add(dictionary1);
        }
        foreach (var item in parts)
        {
            Console.WriteLine($"Class: {item["class"]}, Value: {item["value"]}");
        }
        return parts;
    }

    public List<string> MakeTokens(string line)
    {
        List<string> tokens = new List<string>();
        // if (line[line.Length - 1] != ';')
        // {
        //     // tokens.Add("Error");
        //     return null;
        // }
        string token = string.Empty;
        foreach (var item in line)
        {
            // Console.WriteLine($"item is {item} and is {splittables.Contains(item)}");
            // item = item.toString();
            if (item == ' ')
            {
                if (!string.IsNullOrEmpty(token))
                {
                    tokens.Add(token.Trim());
                }
                token = string.Empty;
            }
            else if (Regex.IsMatch(item.ToString(), "[\"]") || Regex.IsMatch(item.ToString(), "[']"))
            {

                if (!string.IsNullOrEmpty(token))
                {
                    tokens.Add(token.Trim());
                }
                tokens.Add(item.ToString());
                token = string.Empty;

            }
            else if (operators.Contains(item) || punctuators.Contains(item))
            {
                if (!string.IsNullOrEmpty(token))
                {
                    tokens.Add(token.Trim());
                }
                tokens.Add(item.ToString());
                token = string.Empty;

            }
            else
            {
                token += item;
            }

        }
        if (!string.IsNullOrEmpty(token))
        {
            tokens.Add(token);
        }
        makeParts(tokens);
        return tokens;
    }
}



