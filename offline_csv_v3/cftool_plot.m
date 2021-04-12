% Load data from text file and plot surfaces
% gamma Vc Vt c

Data = load("exp_acc_polar.txt");

gamma_lst = Data(:, 1);
Vc_lst = Data(:, 2);
Vt_lst = Data(:, 3);
c_lst = Data(:, 4);

% len = size(gamma_lst);   % size: n * 1
% len = len(1);

% for Vt = [1.5 1.6 1.7 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8]
%     for i = 1:len
%         if Vt_lst(i) == Vt
%             

% Vc = 1;
% error = 0.05;
% edited_gamma = [];
% edited_Vc = [];
% edited_c = [];
% for i = 1:len
%     if Vc_lst(i) >= Vc - error && Vc_lst(i) <= Vc + error
%         edited_gamma = [edited_gamma; gamma_lst(i)];
%         edited_Vc = [edited_Vc; Vc_lst(i)];
%         edited_c = [edited_c; c_lst(i)];
%     end
% end

% scatter(edited_gamma, edited_c);
