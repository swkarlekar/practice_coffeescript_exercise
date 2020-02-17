$ ->
	Grouper =
		data:
			students: {}
			all_possible_groups: {}
			groups: {}
			group_partitions: {}
			my_response: {}

		initialize: ->
			@setStudentData()
			@setNewScreen()

		compute: -> 
			@defineGroupBoundaries()
			@findPermutationsOfStudents()
			@checkPermutations()
			@displayResponse()

		setStudentData: ->
			@data.students = JSON.parse $("input[name='json_input']").val()

		setNewScreen: -> 
			$("form").hide()
			$(".alerts").removeClass("welcome").show()

		displayResponse: -> 
			console.log @data.my_response
			$(".alerts").text("#{JSON.stringify @data.my_response}")

		defineGroupBoundaries: -> 
			num_groups = @data.students.groups
			num_students = @data.students.students.length 
			@data.group_partitions = (x for x in [0..num_students] by Math.floor(num_students/num_groups))[0...-1].concat [num_students]
			console.log "Math.floor(num_students/num_groups): " + Math.floor(num_students/num_groups)
			console.log "x for x in [0..num_students-1]: " + (x for x in [0..num_students])
			console.log "@data.group_partitions " + @data.group_partitions

		findPermutationsOfStudents: ->  
			perm = (xs) ->
				ret = []
				i = 0
				while i < xs.length
					rest = perm(xs.slice(0, i).concat(xs.slice(i + 1)))
					if !rest.length
						ret.push [ xs[i] ]
					else
						j = 0
						while j < rest.length
							ret.push [ xs[i] ].concat(rest[j])
							j = j + 1
					i = i + 1
				ret       
			arr = @data.students.students
			@data.all_possible_groups = perm arr

		checkPermutations: -> 
			group_of_interest = @findFirstValidPermutation()
			if group_of_interest is null
					@data.my_response = 
						error: "UNPOSSIBLE!"
			else
				names_of_group = (student.name for student in group_of_interest)
				@data.my_response = (names_of_group[@data.group_partitions[index]...@data.group_partitions[index+1]] for index in [0...@data.group_partitions.length-1])

		findFirstValidPermutation: -> 
			countNoisy = (xs) -> 
				total_count_noisy = 0
				for student in xs
					if student.noisy == true
						total_count_noisy++; 
				total_count_noisy 
			countUnderstandMaterial = (xs) -> 
				total_count_understands = 0
				for student in xs
					if student.understands == true
						total_count_understands++; 
				total_count_understands
			checkCannotGetAlong = (xs) -> 
				cannotGetAlong = false
				names_in_group = (student.name for student in xs)
				for student in xs
					for opponent in student.fights_with
						if opponent in names_in_group
							cannotGetAlong = true
				cannotGetAlong
			isSubgroupValid = (current_group) -> 
				((countNoisy current_group) <= 2) && ((countUnderstandMaterial current_group) >= 1) && !(checkCannotGetAlong current_group)
			isTrue = (element, index, array) ->
				element
			for group in @data.all_possible_groups
				if (isSubgroupValid group[@data.group_partitions[index]...@data.group_partitions[index+1]] for index in [0...@data.group_partitions.length-1]).every isTrue then return group
			return null

		showAlert: (msg) ->
			$(".alerts").text(msg).slideDown()

	$("form").on "submit", (evt) ->
		evt.preventDefault()
		$inputs = $("input[type='text']")

		dataNotEntered = $inputs.filter(->
			return @value.trim() isnt ""
		).length isnt 1


		if dataNotEntered then Grouper.showAlert("Data cannot be empty")
		else 
			Grouper.initialize() 
			Grouper.compute()
