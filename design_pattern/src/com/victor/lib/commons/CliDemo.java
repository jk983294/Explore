package com.victor.lib.commons;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.GnuParser;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

@SuppressWarnings("static-access")
public class CliDemo {

	public static void main(String[] args) {
		/**
		 * Boolean Options
		 */
		Option help = new Option("help", "print this message");
		Option projecthelp = new Option("projectHelp",
				"print project help information");
		Option version = new Option("version",
				"print the version information and exit");
		Option quiet = new Option("quiet", "be extra quiet");
		Option verbose = new Option("verbose", "be extra verbose");
		Option debug = new Option("debug", "print debugging information");
		Option emacs = new Option("emacs",
				"produce logging information without adornments");

		/**
		 * Argument Options
		 */
		Option logfile = OptionBuilder.withArgName("file").hasArg().withDescription("use given file for log").create("logfile");
		Option logger = OptionBuilder.withArgName("classname").hasArg().withDescription("the class which it to perform " + "logging")
				.create("logger");
		Option listener = OptionBuilder.withArgName("classname").hasArg()
				.withDescription("add an instance of class as " + "a project listener")
				.create("listener");
		Option buildFile = OptionBuilder.withArgName("file").hasArg()
				.withDescription("use given buildFile").create("buildFile");
		Option find = OptionBuilder.withArgName("file").hasArg()
				.withDescription("search for buildFile towards the root of the filesystem and use it")
				.create("find");
		
		/**
		 * Java Property Option
		 */
		Option property  = OptionBuilder.withArgName( "property=value" ).hasArgs(2).withValueSeparator()
                .withDescription( "use value for given property" )
                .create( "D" );
		
		/**
		 * Create the Options
		 */
		Options options = new Options();
		options.addOption( help );
		options.addOption( projecthelp );
		options.addOption( version );
		options.addOption( quiet );
		options.addOption( verbose );
		options.addOption( debug );
		options.addOption( emacs );
		options.addOption( logfile );
		options.addOption( logger );
		options.addOption( listener );
		options.addOption( buildFile );
		options.addOption( find );
		options.addOption( property );
		
		/**
		 * Create the Parser
		 */
		CommandLineParser parser = new GnuParser();
	    try {
	    	String[] argsStrings = new String[]{"f" , "a"};
	        // parse the command line arguments
	        CommandLine cmd = parser.parse( options, args );
	        
	        if(cmd.hasOption("f")) {
	            // print the date and time
	        }
	        else {
	            // print the date
	        }
	        
	        // get c option value
	        String countryCode = cmd.getOptionValue("c");
	        if(countryCode == null) {
	            // print default date
	        }
	        else {
	            // print date for country specified by countryCode
	        }
	    }
	    catch( ParseException exp ) {
	        // oops, something went wrong
	        System.err.println( "Parsing failed.  Reason: " + exp.getMessage() );
	    }
	}
}
