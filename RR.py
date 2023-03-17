def round_robin(processes_lis: list, quantum_time: int):
    burst_list = []
    # copying the burst times because we are going to change it inside the main list
    for lis in processes_lis:
        burst_list.append(lis[2])
    finished = False
    finished_list = []
    queue = []
    time = 0
    ready_processes = 0
    finished_processes = 0
    first_time = False
    while finished_processes < len(processes_lis):
        # add the processes that's ready to the queue
        for process in processes_lis:
            if time >= process[1] and not process[-1]:
                process[-1] = True
                process[3] += time - process[1]
                queue.insert(len(queue), process)
                ready_processes += 1

        # if there is no ready process increment the time
        if ready_processes < 1:
            time += 1
            continue

        # the first element in the queue become the last but not in the first iteration
        if first_time and not finished:
            queue.insert(len(queue), queue.pop(0))

        # if the process burst time is greate than 0
        if queue[0][2] > 0:
            if queue[0][2] > quantum_time:
                # increase the time
                time += quantum_time
                if len(queue) > 1:
                    for i in range(1, len(queue)):
                        # add the quantum time to every waiting time in the queue
                        queue[i][3] += quantum_time
                # increase the time
                # decrease the burst time for the process we already worked on
                queue[0][2] -= quantum_time
                finished = False
            else:
                # increase the time
                time += queue[0][2]
                if len(queue) > 1:
                    for i in range(1, len(queue)):
                        # add the burst time to every waiting time in the queue
                        queue[i][3] += queue[0][2]
                # decrease the burst time for the process we already worked on
                queue[0][2] -= queue[0][2]
                # set the completion time
                queue[0][5] = time
                # set the turnaround time
                queue[0][4] = time - queue[0][1]
                finished_processes += 1
                ready_processes -= 1
                finished = True
                finished_list.append(queue.pop(0))
        first_time = True

    # sort the final list with name, so we can print a suitable table for UX
    finished_list.sort(key=lambda x: x[1])

    # get the total waiting time
    total_waiting_time = 0
    for i in range(len(finished_list)):
        total_waiting_time += finished_list[i][3]

    # get the total turnaround time
    total_turnaround_time = 0
    for i in range(len(finished_list)):
        total_turnaround_time += finished_list[i][4]

    avg_waiting_time = total_waiting_time / len(finished_list)
    avg_turnaround_time = total_turnaround_time / len(finished_list)

    print("Process\t\tArrival Time\t\tBurst Time\t\tCompletion Time\t\tWaiting Time\t\tTurnaround Time")
    for i in range(len(finished_list)):
        print(
            f"{finished_list[i][0]}\t\t\t\t{finished_list[i][1]}\t\t\t\t\t{burst_list[i]}\t\t\t\t\t{finished_list[i][5]}"
            f"\t\t\t\t{finished_list[i][3]}\t\t\t\t\t{finished_list[i][4]}")
    print("\nAverage Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)


if __name__ == '__main__':
    processes_list = []
    quantum = int(input("enter the quantum time : "))
    for i in range(int(input("enter the number of the processes : "))):
        process_list = [0] * 7
        process_list[0] = f"P{i + 1}"
        process_list[1] = int(input(f"enter {process_list[0]} arrival : "))
        process_list[2] = int(input(f"enter {process_list[0]} burst : "))
        process_list[-1] = False
        processes_list.append(process_list)
    round_robin(processes_list, quantum)
    # process_list = [0 process_name, 1 arrival_time, 2 burst_time, 3 waiting_time, 4 turnaround_time,  5 completion_time, 6 false (didn't go to queue)]
