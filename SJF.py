def shortest_job_first(processes_lis: list):
    burst_list = []
    # copying the burst times because we are going to change it inside the main list
    for lis in processes_lis:
        burst_list.append(lis[2])
    time = 0
    queue = []
    finished_processes = 0
    ready_processes = 0
    finished_list = []

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

        # sort the queue ascending according to the burst time then arrival time
        queue.sort(key=lambda x: (x[2], x[1]))

        if queue[0][2] > 0:
            time += queue[0][2]
            # add waiting time to every process that's waiting in the queue
            for i in range(1, len(queue)):
                queue[i][3] += queue[0][2]
            # set the completion time to the process we finished
            queue[0][5] = time
            # set the turnaround time to the process we finished
            queue[0][4] = time - queue[0][1]
            ready_processes -= 1
            finished_processes += 1
            finished_list.append(queue.pop(0))

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
    for i in range(int(input("enter the number of the processes : "))):
        process_list = [0] * 7
        process_list[0] = f"P{i + 1}"
        process_list[1] = int(input(f"enter {process_list[0]} arrival : "))
        process_list[2] = int(input(f"enter {process_list[0]} burst : "))
        process_list[-1] = False
        processes_list.append(process_list)
    shortest_job_first(processes_list)
    # process_list = [0 process_name, 1 arrival_time, 2 burst_time, 3 waiting_time, 4 turnaround_time,  5 completion_time, 6 false (didn't go to queue)]
