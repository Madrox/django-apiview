django-apiview
==============

A lightweight decorator to make it easy to create json-based API views in django. It should abstract away most of the common input and output scrubbing. The decorator is designed to be very forgiving of what gets returned from the view and not produce output that an API consumer couldn't easily handle.

## Basic Usage

```from apiview import api_view

@api_view
def djangoview(request):
	return 'hello'```

This will produce a response with a mime type of `application/json` where the output of .

```{
	data: "hello",
	run_time: 0.000011
}```

## Features

### Data types

The decorator will attempt to serialize anything. If all else fails, it will resort to django's `force_text` function.

### Run Time

By default, a run_time property is returned with the time it took to run the view function in seconds.

```from apiview import api_view

@api_view(show_run_time=False) # DISABLE THE run_time PROPERTY
def djangoview(request):
	return { 'foo': 'bar' }```

This will produce

```{
	data: {
		foo: "bar"
	}
}```

### Usage Information

Usage information can be passed to the decorator. This is handy if you'd like to give API users hints about how to interface with your API. If this is passed, all required fields will be checked to exist before calling the view. If any fields are missing, the usage JSON will be returned instead as a HTTP 400.

```@api_view(usage={ 'name': (True, 'A required field'), 'hello': (False, 'An optional parameter to pass') })
def djangoview(request):
	return { 'foo': 'bar' }```

In this example, `name` is required in the query string. `hello` is optional.

Similar to `show_run_time`, you can have the output display the usage information in the view. This is on by default, to disabel it, pass `show_usage=False`

### JSON-P

The decorator will handle json-p requests for you by default. If a user calls an endpoint with `callback` in the query string, it will handle it appropriately and switch the mime type to `application/javascript`.

To disable json-p support, pass `json=False`.

