def generate_serializer_errors(args):
	message = ''
	for key,values in args.iteritems():
		error_message = ""
		for value in values:
			error_message +=value + ","
		error_message = error_message[:-1]

		message += "%s : %s |" %(key,error_message)
	return message[:-3]
