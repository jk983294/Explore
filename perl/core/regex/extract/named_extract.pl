#!/usr/bin/perl
use strict;
use warnings;

# (?<LABEL>PATTERN),data saved in %+
if ( 'hello there, kun' =~ /(?<name1>\S+)\s(?<name2>\S+),\s(?<name3>\S+)/ ) {
    print "$+{name1}, $+{name2}, $+{name3}\n";
}

# reverse reference \k<LABEL>
if ( 'abc def abc' =~ /(?<name1>\S+)\s(?<name2>\w+)\s\k<name1>/ ) {
    print "$+{name1}, $+{name2}\n";
}
