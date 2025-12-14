Output demo.gif

Set FontSize 22
Set Width 1200
Set Height 600
Set Theme "Catppuccin Mocha"

Set Shell zsh
Hide
Type "export PS1='> '"
Enter
Type "clear"
Enter
Show

Type "pd columns data.csv"
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show

Type "pd select name,price data.csv"
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show

Type "pd sort price data.csv --descending | pd head"
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show

Type `pd query "price > 4.5" data.csv --json`
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show

Type "pd value-counts category data.csv --format md"
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show

Type "pd groupby category data.csv --col stock --agg sum -f md"
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show

Type "pd batch data.csv --sizes 1,2 -o 'batch_{}.csv'"
Sleep 500ms
Enter
Sleep 3.5s
Hide
Type "clear"
Enter
Show
