using System;
using System.Text;

namespace CompilerCons
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 1)
            {
                string[] st = args[0].Split(".");
                var ext = st[st.Length - 1];
                if (ext == "tinkx")
                {
                    Console.WriteLine("File accepted");
                    using (StreamReader reader = new StreamReader(args[0]))
                        {
                            Console.WriteLine($"Reading lines from file: {args[0]}");
                            string line;
                            int count=0;
                            while ((line = reader.ReadLine()) != null)
                            {
                                count+=1;
                                var tokens=new Tokenization().MakeTokens(line);
                                // if(tokens==null){
                                //     Console.WriteLine($"Error at line {count}");
                                //     break;
                                // }
                            }
                        }
                }
                else
                {
                    Console.WriteLine("File extension is not recognized");
                }
            }
            else
            {
                Console.WriteLine("No file provided.");
            }
        }
    }
}
